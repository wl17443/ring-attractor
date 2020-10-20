__revise_mode__ = :eval
using DifferentialEquations
using StaticArrays


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


function normal_divergence(n1, n2)
    log(n2.σ/n1.σ) + (n1.σ^2 + (n1.μ - n2.μ)^2) / (2*n2.σ^2) - 0.5
end


function divergence(V)
    spikes = V .== 0
    spikes = broadcast(*, spikes, [1:1:np.N;])
    slice_1 = spikes[:, 1:3000]
    slice_1 = reshape(slice_1, :)
    slice_1 = slice_1[slice_1 .> 0]

    slice_2 = spikes[:, 7000:end]
    slice_2 = reshape(slice_2, :)
    slice_2 = slice_2[slice_2 .> 0]
    
    N₁ = fit(Normal, slice_1)
    N₂ = fit(Normal, slice_2)

    normal_divergence(N₁, N₂)
end


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
    
    cm .*= np.kₛ .* 1e-6
    cm[cm .< 0] .*= -(1 - np.Eᵢ)
	return SMatrix{np.N, np.N}(cm)
end







### Block of 3 functions to simulate network ###


# This function initializes all the needed arrays
function simulate(time, cm, np, dt)
	V = MMatrix{np.N, time}(zeros(np.N, time))
	sd = MMatrix{np.N, time}(zeros(np.N, time))
	sd .+= [dt:dt:dt*time;]'

	sd .+= 2.
    V[:, 1] .= np.Vᵣ

	# give current
    for t in 1:time-3
        step!(V, sd, t, cm, np, dt)
	
    end
    
    V
end


# This function checks for spikes, update one column of the V and of spike delays
function step!(V, sd, t, cm, np, dt)

	dv!(view(V, :, t), sd[:, t], cm, np, dt) # This could actually slow down

    V[view(V,:, t) .> np.Vₜ, t+1] .= 0.0
    V[view(V,:, t) .== 0, t+1] .= np.Vᵣ
    
    sd[view(V,:, t) .> np.Vₜ, t+3] .= dt*3 # TODO: make this indepentend from dt

end


# This function updates the V given the spike delays
function dv!(v, sd, cm, np, dt)

    I = (cm .* sd .* exp.(-sd ./ np.τₛ)) * v
    v .+= (-np.Cₘ / np.τₘ .* (v .- np.Eₗ) .- I) ./ np.Cₘ .* dt # .+ rand(Normal(0, noise), np.N)
   	 
end



### Block of 3 functions to simulate with DifferentialEquations ###


function DEsimulate(time, cm, np, dt)
	alg = FunctionMap{true}()

    V = zeros(np.N, time)
	spiked = zeros(np.N, time) .+ [dt:dt:dt*time;]'

    V[:, 1] .= np.Vᵣ

	# give current
    for t in 1:time-3
        DEstep!(V, spiked, t, cm, np, dt, alg)
	
    end
    
    V
end


function DEstep!(V, sd, t, cm, np, dt, alg)
   	 
	p = (sd[:, t], np)
	prob = DiscreteProblem(f, V[:, t], (0, dt), p)
	solve(prob, alg)

    V[view(V,:, t) .> np.Vₜ, t+1] .= 0.0
    V[view(V,:, t) .== 0, t+1] .= np.Vᵣ
    
    sd[view(V,:, t) .> np.Vₜ, t+3] .= dt*3

end

function f(u, p, t)
	I = (cm .* p[1] .* exp.(-p[1] ./ p[2].τₛ)) * u
	return (-p[2].Cₘ / p[2].τₘ .* (u .- p[2].Eₗ) .- I) ./ p[2].Cₘ
end


const cm = make_connectivity_matrix(sp, np);

# We're down to 74 allocations for time=10, dv takes virtually the whole time
