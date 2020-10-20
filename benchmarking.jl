using Distributions

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
	ms::Float64
	mV::Float64
	nF::Float64
	dt::Float64
	noise::Float64
	fps::Tuple
end

ep = EnvironmentParameters(1e-3, 1e-3, 1e-9, 1e-3, 2e-3, ())
np = NeuronParameters(256, -48. *ep.mV, -80. *ep.mV, 1. *ep.nF, -70. *ep.mV, 0., -70. *ep.mV, -70. *ep.mV, 2.  *ep.ms, 5. *ep.ms, 5. *ep.ms, 1/(5*ep.ms*exp(-1.)))
sp = SynapseParameters(5, 7, 0.05, -0.10, 0.05, -0.25, 3)

const Eₗₜ= np.Eₗ / np.τₘ


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
function simulate(tottime, np, sp, ep)
	w = genweights(np, sp)
    V = zeros(np.N, tottime)
	# sd = zeros(np.N, tottime) .+ [0:1:tottime-1;]' .* ep.dt .+ 0.2
	sd = zeros(np.N) .+ 0.2

    V[:, 1:4] .= np.Vᵣ
	V[126:132,1:4] .= 0.

    for t in 3:tottime-1
        step!(V, sd, t, w, np, ep, tottime)
    end

    V[:, 1:tottime], sd
end

# This function checks for spikes, update one column of the V and of spike delays
function step!(V, sd, t, w, np, ep, tottime)



	V[:, t+1] = dv(view(V, :, t), sd, w, np, ep)
	V[view(V,:, t) .> np.Vₜ, t+1] .= 0.0
	V[view(V,:, t) .== 0.0, t+1] .= np.Vᵣ

	sd .+= ep.dt
	sd[view(V,:, t-2) .== 0.0] .= 0.
	end
	# sd[view(V,:, t) .== 0.0, t+2:end] .= [2:1:tottime-t;]'.*ep.dt; # substitute 2 with refractory period variable
end


function dv(v, sd, w, np, ep)
	# variable for exp?
	k = sd .* exp.(-sd ./ np.τₛ)
	v.+ ((Eₗₜ .- v ./ np.τₘ ).- (v.-np.Eₑ) .*( w[2] * k) .- (v.-np.Eᵢ) .*( w[1] * k)) .* ep.dt .+ rand(Normal(0, 1.3e-3), np.N)
end


pot, sd = simulate(10000, np, sp, ep)
