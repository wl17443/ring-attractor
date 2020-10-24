using Distributions
using LinearAlgebra
using Plots

struct NeuronParameters
    N::Int64
    Vₜ::Float64
    Vᵣ::Float64
    Cₘ::Float64
    Eᵢ::Float64
    Eₑ::Float64
    Eₘ::Float64
    Eₗ::Float64
    τᵣ::Float64
    τₛ::Float64
    τₘ::Float64
    kₛ::Float64
end

struct SynapseParameters
    n_exc::Int64
    n_inh::Int64
    w_exc::Float64
    w_inh::Float64
    w_exc_fp::Float64
    w_inh_fp::Float64
    fp_width::Int64
end

struct EnvironmentParameters
	time::Int64
	ms::Float64
	mV::Float64
	nF::Float64
	dt::Float64
	noise::Float64
	fps::Tuple
end

ep = EnvironmentParameters(10000, 1e-3, 1e-3, 1e-9, 1e-3, 1e-3, ())
np = NeuronParameters(64, -48. *ep.mV, -80. *ep.mV, 1. *ep.nF, -70. *ep.mV, 0., -70. *ep.mV, -70. *ep.mV, 2.  *ep.ms, 5. *ep.ms, 5. *ep.ms, 1/(5*ep.ms*exp(-1.)))
sp = SynapseParameters(5, 7, 0.05, -0.10, 0.05, -0.25, 3)

const Eₗₜ= np.Eₗ / np.τₘ


function sliding_filter(V, bin=100)
    spikes = Array{Int, 2}(V .== 0)
    spikes .*= [1:1:np.N;]
    normes = zeros((ep.time ÷ bin) -1)

    for i in 1:ep.time÷bin-1
        s1_var, s1_mean, s1_fit = slide_measures(view(spikes, :, i:i*bin))
        s2_var, s2_mean, s2_fit = slide_measures(view(spikes, :, i*bin:i*(bin+1)))
        normes[i] = norm([abs(s1_var - s2_var), abs(s1_mean - s2_mean), kl_divergence(s1_fit, s2_fit)])
    end
    mean(normes), var(normes)
end

function slide_measures(s)

    vert_mean = mean(s, dims=1)
    s_var = var(vert_mean)
    s_mean = mean(vert_mean)
    s_fit = fit(Normal, view(s, s .> 0))

    s_var, s_mean, s_fit
end

function kl_divergence(n1, n2)
    log(n2.σ/n1.σ) + (n1.σ^2 + (n1.μ - n2.μ)^2) / (2*n2.σ^2) - 0.5
end


# This makes a np.N x np.N matrix of weights, mostly zeros
function genweights(np::NeuronParameters, sp::SynapseParameters)
    w = zeros(Float64, np.N,np.N)
    for i in 1:np.N
        for k in 1:np.N
            dist = abs(i - k)
            w[i, k] = min(np.N - dist, dist)
        end
    end
    w[1 .<= w .<= sp.n_exc] .= sp.w_exc
    w[sp.n_exc .< w .<= sp.n_exc+sp.n_inh] .= sp.w_inh
    w[w .> sp.n_exc+sp.n_inh] .= 0.

    if length(ep.fps) > 0
        for i in ep.fps
            x = w[i, :]
            x[x .== sp.w_exc] .= sp.w_exc_fp
            x[x .== sp.w_inh] .= sp.w_inh_fp
            w[i, :] = x
        end
    end
	w .*= np.kₛ * 1e-6 / np.Cₘ
	w_inh = deepcopy(w)
	w_exc = deepcopy(w)

	w_inh[w .> 0] .= 0
	w_inh[w .< 0] *= -1
	w_exc[w .< 0] .= 0

    return w_inh, w_exc
end


# This function initializes all the needed arrays
function simulate(np, sp, ep)
	w = genweights(np, sp)
    V = zeros(np.N, 4+ep.time)

	sd = fill!(zeros(np.N), 0.2)

    replace!(view(V, :, 1:4), 0. => np.Vᵣ)
	replace!(view(V, 30:36, 3), np.Vᵣ => 0.) # This has to be a variable

    for t in 3:ep.time+3
        step!(V, sd, t, w, np, ep)
    end

    V[:, 3:ep.time+2]
end

# This function checks for spikes, update one column of the V and of spike delays
function step!(V, sd, t, w, np, ep)
	V[:, t+1] = dv(view(V, :, t), sd, w, np, ep)
	V[view(V,:, t) .> np.Vₜ, t+1] .= 0.0
	V[view(V,:, t) .== 0.0, t+1] .= np.Vᵣ

	sd .+= ep.dt
	sd[view(V,:, t-2) .== 0.0] .= 0.
end


function dv(v, sd, w, np, ep)
	# variable for exp?
	k = sd .* exp.(-sd ./ np.τₛ)
	v.+ ((Eₗₜ .- v ./ np.τₘ ).- (v.-np.Eₑ) .*( w[2] * k) .- (v.-np.Eᵢ) .*( w[1] * k)) .* ep.dt .+ rand(Normal(0, ep.noise), np.N)
end
