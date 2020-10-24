# using Distributions
using DifferentialEquations
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
function DEsimulate(tottime, np, sp, ep)
	alg = FunctionMap{true}()
	w = genweights(np, sp)
    v = zeros(np.N) .+ np.Vᵣ
	sd = zeros(np.N) .+ 0.2

	v[1:5] .= 0.

	p = (w, np, ep)
	prob = DiscreteProblem(update!, [v, sd], (ep.dt, tottime*ep.dt), p)
	sim = solve(prob, alg, dt=ep.dt)
	return sim

end



function update!(dv, u, p, t)
	w, np, ep = p

	v, sd = u
	v[v .== 0.0] .= np.Vᵣ
	v[v .> np.Vₜ] .= 0.0

	k = sd .* exp.(-sd ./ np.τₛ)
	dv[1] += ((Eₗₜ .- v ./ np.τₘ ).- (v.-np.Eₑ) .*( w[2] * k) .- (v.-np.Eᵢ) .*( w[1] * k))
	dv[2][v .== 0.0] .= 2*ep.dt
	dv[2] .+= 1
end


sim = DEsimulate(200, np, sp, ep)
