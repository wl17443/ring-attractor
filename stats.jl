using Distributions
using LinearAlgebra

function sliding_filter(V, sim,  bin=100, step=50)
	start = 6600 # compute it
    spikes = Array{Float64, 2}(V[:, start:end] .== 0)
    spikes .*= [1:1:sim.N;]
    normes = zeros(Float64, (3400 ÷ step) -1)


	for i in 0:(3400-3step)÷step
        s1_var, s1_mean, s1_fit = slide_measures(view(spikes, :, 1+i*step:1+i*step+bin))
        s2_var, s2_mean, s2_fit = slide_measures(view(spikes, :, 1+(1+i)*step:1+(1+i)*step+bin))
        normes[i+1] = norm([abs(s1_var - s2_var), abs(s1_mean - s2_mean), kl_divergence(s1_fit, s2_fit)])
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
