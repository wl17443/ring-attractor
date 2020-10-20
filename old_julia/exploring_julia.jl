# using Distributions
# using Plots
using ProfileView

ms = 1e-3
mV = 1e-3
nF = 1e-9

# z = Normal(0, 1e-3)
fps = (3, 7)
dt = ms

struct NeuronParameters
    N::Int64
    Vₜ
    Vᵣ
    Cₘ
    Eᵢ
    Eₑ
    Eₘ
    Eₗ
    τᵣ
    τₛ
    τₘ
    kₛ
end

struct SynapseParameters
    n_exc
    n_inh
    w_exc
    w_inh
    w_exc_fp
    w_inh_fp
    fp_width
end

np = NeuronParameters(20, -48. *mV, -80. *mV, 1. *nF, -70. *mV, 0., -70. *mV, -70. *mV, 2.  *ms, 5. *ms, 5. *ms, 1/(5*ms*exp(-1.)))
sp = SynapseParameters(5, 7, 0.05, -0.10, 0.06, -0.25, 3)

function make_connectivity_matrix(sp::SynapseParameters, np::NeuronParameters)
    cm = zeros(Float64, np.N,np.N)
    for i in 1:np.N
        for k in 1:np.N
            dist = abs(i - k)
            cm[i, k] = min(np.N - dist, dist)
        end
    end
    cm[1 .<= cm .<= sp.n_exc] .= sp.w_exc
    cm[cm .> sp.n_exc] .= sp.w_inh
    
    if length(fps) > 0
        for i in fps
            x = cm[i, :]
            x[x .== sp.w_exc] .= sp.w_exc_fp
            x[x .== sp.w_inh] .= sp.w_inh_fp
            cm[i, :] = x
        end
    end
    cm
end

function dv(v, sd, cm)
    Iᵢ = zeros(Float64, np.N)
    Iₑ = zeros(Float64, np.N)

    for i in 1:np.N
        inh = Float32[]
        exc = Float32[]

        I_array = cm[:, i] .* sd .* np.kₛ .* exp.(-sd ./ np.τₛ) .* 1e-6
        for I in I_array
            if I < 0
                push!(inh, -I.*(v[i] - np.Eᵢ))
            else
                push!(exc, I * (v[i] - np.Eₑ))
            end
        end
        Iᵢ[i] = sum(inh)
        Iₑ[i] = sum(exc)
    end

    δv = (-np.Cₘ / np.τₘ .* (v .- np.Eₗ) .- Iᵢ .- Iₑ) ./ np.Cₘ .* dt # .+ rand(z, length(v))
    
    return δv+v
end

function step(potentials, spike_delays, cm)
    t = size(potentials, 2)
    
    to_depolarize = potentials[:, t] .> np.Vₜ
    to_hyperpolarize = potentials[:, t] .== 0
    
    potentials = [potentials dv(potentials[:, t], spike_delays, cm)] # This looks inefficient
    tmp = potentials[:, t+1]
    tmp[to_depolarize] .= 0.0
    tmp[to_hyperpolarize] .= np.Vᵣ
    potentials[:, t+1] = tmp
    
    
    
    spike_delays .+= dt
    spike_delays[to_depolarize] .= 0.0

    potentials, spike_delays
end

function simulate(time)
    cm = make_connectivity_matrix(sp, np)
    pot = zeros(Float64, np.N) .+ np.Vᵣ
    spiked = zeros(Float64, np.N) .+ 2
    spiked[9:11] .= 0
    for t in 1:time
        pot, spiked = step(pot, spiked, cm)
    end
    
    pot
end

@profview simulate(1)

# pots = simulate(100, true)
# heatmap(pots)

# spikes = pots .== 0
# spikes = broadcast(*, spikes, [1:1:20;])
# slice = spikes[:, 1:30]

# slice = reshape(slice, :)
# slice = slice[slice .> 0]

# fit(Normal, slice)


