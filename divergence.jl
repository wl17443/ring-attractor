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

