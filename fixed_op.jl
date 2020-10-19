# using Distributions
# using Plots
__revise_mode__ = :eval


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


const ep = EnvironmentParameters(1e-3, 1e-3, 1e-9, 1e-3, 2e-3, (3, 7))
const np = NeuronParameters(256, -48. *ep.mV, -80. *ep.mV, 1. *ep.nF, -70. *ep.mV, 0., -70. *ep.mV, -70. *ep.mV, 2.  *ep.ms, 5. *ep.ms, 5. *ep.ms, 1/(5*ep.ms*exp(-1.)))
const sp = SynapseParameters(5, 7, 0.05, -0.10, 0.06, -0.25, 3)

const Eₗₜ= np.Eₗ / np.τₘ


# This makes a np.N x np.N matrix of weights, mostly zeros
function make_connectivity_matrix(sp::SynapseParameters, np::NeuronParameters)
    cm = zeros(Float64, np.N,np.N)
    for i in 1:np.N
        for k in 1:np.N
            dist = abs(i - k)
            cm[i, k] = min(np.N - dist, dist)
        end
    end
    cm[1 .<= cm .<= sp.n_exc] .= sp.w_exc
    cm[sp.n_exc .< cm .<= sp.n_exc+sp.n_inh] .= sp.w_inh
    cm[cm .> sp.n_exc+sp.n_inh] .= 0.

    if length(ep.fps) > 0
        for i in ep.fps
            x = cm[i, :]
            x[x .== sp.w_exc] .= sp.w_exc_fp
            x[x .== sp.w_inh] .= sp.w_inh_fp
            cm[i, :] = x
        end
    end
    #  cm[cm .> 0] .*= (1 - np.Eₑ) # Not needed np.Eₑ == 1

	cm .*= np.kₛ * 1e-6 / np.Cₘ
    cm[cm .< 0] .*= -np.Eᵢ
    return cm
end


### Block of 3 functions to simulate network ###


# This function initializes all the needed arrays
function simulate(tottime, cm, np, ep)
    V = zeros(np.N, tottime)
	sd = zeros(np.N, tottime) .+ [ep.dt:ep.dt:ep.dt*tottime;]'

	sd .+= 2
    V[:, 1] .= np.Vᵣ

	# give current
    for t in 1:tottime-3
        step!(V, sd, t, cm, np, ep, tottime)
    end

    V[:, 1:tottime-3], sd[:, 1:tottime-3]
end


# This function checks for spikes, update one column of the V and of spike delays
function step!(V, sd, t, cm, np, ep, tottime)

	V[:, t+1] = dv(view(V, :, t), view(sd, :, t), cm, np, ep) # View could actually slow down

    V[view(V,:, t) .> np.Vₜ, t+1] .= 0.0
    V[view(V,:, t) .== 0, t+1] .= np.Vᵣ
    
	sd[view(V,:, t) .== 0.0, t+Int(3*(ep.dt÷ep.ms)):end] .= [ep.dt*3:ep.dt:ep.dt*(tottime-t+2*ep.ms);]'
end


# This function updates the V given the spike delays
function dv(v, sd, cm, np, ep)
	v .+ (Eₗₜ .- v ./ np.τₘ .- (v .*( cm * (sd .* exp.(-sd ./ np.τₛ))))) * ep.dt
end

const cm = make_connectivity_matrix(sp, np)

pot, sd = simulate(10, cm, np, ep)
@show pot
