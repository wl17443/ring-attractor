using Distributions
using Random

struct FixedParameters
	# Neuron
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
	Eₗₜ::Float64

	# Connectivity
    n_exc::Int64
    n_inh::Int64
    fp_width::Int64

	# Measures
	ms::Float64
	mV::Float64
	nF::Float64
	dt::Float64
end

struct SimulationParameters
    N::Int64
	time::Int64
	noise::Float64
	fps::Tuple
	seed::Int64
    w_exc::Float64
    w_inh::Float64
    w_exc_fp::Float64
    w_inh_fp::Float64
end

const par=FixedParameters(-48e-3, -80e-3, 1e-9, -70e-3, 0., -70e-3, -70e-3, 2e-3, 5e-3, 5e-3, 1/(5e-3*exp(-1.)), -70.0/5., 5, 7, 3, 1e-3, 1e-3, 1e-9, 1e-3)
# sim=SimulationParameters(64, 10000, 5e-4, (26, 38), 0, 0.05, -0.10, 0.05, -0.25)


# This function initializes all the needed arrays
function simulate(par, sim)
	if sim.seed != 0
		Random.seed!(sim.seed)
	end
	w = genweights(par, sim)
    V = zeros(sim.N, 4+sim.time)

	sd = fill!(zeros(sim.N), 0.2)

    replace!(view(V, :, 1:4), 0. => par.Vᵣ)
	replace!(view(V, 30:35, 3), par.Vᵣ => 0.) # This has to be a variable

    for t in 3:sim.time+3
        step!(V, sd, t, w, par, sim)
    end

    V[:, 3:sim.time+2]
end

# This function checks for spikes, update one column of the V and of spike delays
function step!(V, sd, t, w, par, sim)
	V[:, t+1] = dv(view(V, :, t), sd, w, par, sim)
	V[view(V,:, t) .> par.Vₜ, t+1] .= 0.0
	V[view(V,:, t) .== 0.0, t+1] .= par.Vᵣ

	sd .+= par.dt
	sd[view(V,:, t-2) .== 0.0] .= 0.
end


function dv(v, sd, w, par, sim)
	k = sd .* exp.(-sd ./ par.τₛ)
	v.+ ((par.Eₗₜ .- v ./ par.τₘ ).- (v.-par.Eₑ) .*( w[2]' * k) .- (v.-par.Eᵢ) .*( w[1]' * k)) .* par.dt .+ rand(Normal(0, sim.noise), sim.N)
end


# This makes a sim.N x sim.N matrix of weights, mostly zeros
function genweights(par::FixedParameters, sim::SimulationParameters)
    w = zeros(Float64, sim.N,sim.N)
    for i in 1:sim.N
        for k in 1:sim.N
            dist = abs(i - k)
            w[i, k] = min(sim.N - dist, dist)
        end
    end
    w[1 .<= w .<= par.n_exc] .= sim.w_exc
    w[par.n_exc .< w .<= par.n_exc+par.n_inh] .= sim.w_inh
    w[w .> par.n_exc+par.n_inh] .= 0.

    if length(sim.fps) > 0
        for i in sim.fps
			r= i-par.fp_width÷2:i+par.fp_width÷2+1
			replace!(view(w, r, :), sim.w_exc => sim.w_exc_fp)
			replace!(view(w, r, :), sim.w_inh => sim.w_inh_fp)

        end
    end
	w .*= par.kₛ * 1e-6 / par.Cₘ
	w_inh = deepcopy(w)
	w_exc = deepcopy(w)

	w_inh[w .> 0] .= 0
	w_inh[w .< 0] *= -1
	w_exc[w .< 0] .= 0

    return w_inh, w_exc
end
