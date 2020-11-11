using DrWatson
@quickactivate "Ring Attractor"

using Distributions
using LinearAlgebra

function sim_and_measure(ring::Ring)
    ring()
    sliding_filter(ring)
end

function sliding_filter(ring::Ring, bin=100, step=50)
    # start = 6600 # compute it
    spikes = convert(Array{Float64, 2}, ring.S)
    spikes .*= [1:1:ring.N;]
    normes = zeros(Float64, (10000 ÷ step))


	for (k, i) in enumerate(1:step:size(spikes, 2) - 2bin)
        s1_var, s1_mean, s1_fit = slide_measures(view(spikes, :, i:i+bin))
        s2_var, s2_mean, s2_fit = slide_measures(view(spikes, :, i+bin:i+2bin))
        normes[k] = norm([abs(s1_var - s2_var), abs(s1_mean - s2_mean), kl_divergence(s1_fit, s2_fit)])
    end
    mean(normes), var(normes)
end

function slide_measures(s)
    vert_mean = mean(s, dims=1) #TODO Do we prefer to keep 0s?
    s_var = var(vert_mean)
    s_mean = mean(vert_mean)
    s_fit = fit(Normal, s)

    s_var, s_mean, s_fit
end

function kl_divergence(n1, n2)
    log(n2.σ/n1.σ) + (n1.σ^2 + (n1.μ - n2.μ)^2) / (2*n2.σ^2) - 0.5
end



function slice(spikes, range)
	spikes = Array{Int, 2}(spikes)
	spikes[:, range] .*= [1:1:size(spikes, 1);]
    @view spikes[spikes .> 0]
end

function skipnan(v::AbstractArray)
    v[.!isnan.(v)]
end