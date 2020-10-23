using Distributions
using LinearAlgebra

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

#
# function slice(spikes, t1, t2)
#     s = spikes[:, t1:t2]
#     view(s, s .> 0)
# end
#
#
# function total_divergence(spikes)
#     spikes = Array{Int, 2}(V .== 0)
#     spikes .*= [1:1:np.N;]
#
#     slice_1 = spikes[:, 1:3000]
#     slice_1 = reshape(slice_1, :)
#     slice_1 = slice_1[slice_1 .> 0]
#
#     slice_2 = spikes[:, 7000:end]
#     slice_2 = reshape(slice_2, :)
#     slice_2 = slice_2[slice_2 .> 0]
#
#     N₁ = fit(Normal, slice_1)
#     N₂ = fit(Normal, slice_2)
#
#     normal_divergence(N₁, N₂)
# end
