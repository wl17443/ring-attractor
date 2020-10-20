# using Distributions
# using Plots

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

const ms = 1e-3
const mV = 1e-3
const nF = 1e-9

const fps = (3, 7)
const dt = 1e-3
const noise = 2e-3

const np = NeuronParameters(256, -48. *mV, -80. *mV, 1. *nF, -70. *mV, 0., -70. *mV, -70. *mV, 2.  *ms, 5. *ms, 5. *ms, 1/(5*ms*exp(-1.)))
const sp = SynapseParameters(5, 7, 0.05, -0.10, 0.06, -0.25, 3)

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
    
    if length(fps) > 0
        for i in fps
            x = cm[i, :]
            x[x .== sp.w_exc] .= sp.w_exc_fp
            x[x .== sp.w_inh] .= sp.w_inh_fp
            cm[i, :] = x
        end
    end
    #  cm[cm .> 0] .*= (1 - np.Eₑ) # Not needed np.Eₑ == 1
    
    cm .*= np.kₛ .* 1e-6
    cm[cm .< 0] .*= -(1 - np.Eᵢ)


    return cm
end

function dv(v, sd)

    I = (cm .* sd .* exp.(-sd ./ np.τₛ)) * v
    δv = (-np.Cₘ / np.τₘ .* (v .- np.Eₗ) .- I) ./ np.Cₘ .* dt # .+ rand(Normal(0, noise), np.N)
    
    return δv+v
end

function step(potentials, spike_delays, t)::Tuple{Array{Float64, 2}, Array{Float64, 1}}
    
    # This is to make time delay, not sure it is useful
    # It should work as in the python code though
    delayed_delays = deepcopy(spike_delays)
    delayed_delays[spike_delays .<= 2*ms] .= 2 

    
    to_depolarize = potentials[:, t] .> np.Vₜ
    to_hyperpolarize = potentials[:, t] .== 0
    
    potentials[:, t+1] = dv(potentials[:, t], delayed_delays) 
    tmp = potentials[:, t+1]
    tmp[to_depolarize] .= 0.0
    tmp[to_hyperpolarize] .= np.Vᵣ
    potentials[:, t+1] = tmp
    
    spike_delays = spike_delays .+ dt
    spike_delays[to_depolarize] .= 0.0

    potentials, spike_delays
end

function simulate(time)
    pot = zeros(Float64, np.N, time) 
    pot[:, 1] .+= np.Vᵣ
    spiked = zeros(Float64, np.N) .+ 2.
    spiked[127:129] .= 0.00
    for t in 1:time-1
        pot, spiked = step(pot, spiked, t)
    end
    
    pot
end

function normal_divergence(n1, n2)
    log(n2.σ/n1.σ) + (n1.σ^2 + (n1.μ - n2.μ)^2) / (2*n2.σ^2) - 0.5
end

function divergence(pot)
    spikes = pot .== 0
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

cm = make_connectivity_matrix(sp, np);


simulate(10);
# pot=simulate(10000);
# divergence(pot)
# heatmap(pot)
