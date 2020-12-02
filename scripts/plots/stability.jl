using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()
using StatsPlots
using DataFrames 

include(srcdir("plots.jl"))

# Stability range for weights without noise
m = wload(datadir("stability", "network", "sum","stability/hebb/h0=0_h1=0_n0=0_n1=0.002_seed=2020_nn=500_nh=500.csv")) |> DataFrame
m = m[0.05 .< m.exc .< 0.13, :]
scatter_w_range(m, "Stability range for weights without noise")

# Weights in low points
inspect_weights(wₑ=0.051, wᵢ=0.2, noise=0.)
inspect_weights(wₑ=0.112, wᵢ=0.197, noise=0.)

# Weird weights in critical range:
inspect_weights(wₑ=0.092, wᵢ=0.166, noise=0.)
inspect_weights(wₑ=0.063, wᵢ=0.063, noise=0.)
inspect_weights(wₑ=0.064, wᵢ=0.075, noise=0.)
inspect_weights(wₑ=0.093, wᵢ=0.163, noise=0.)
inspect_weights(wₑ=0.114, wᵢ=0.194, noise=0.)
inspect_weights(wₑ=0.048, wᵢ=0.135, noise=0.)
inspect_weights(wₑ=0.087, wᵢ=0.142, noise=0.)
inspect_weights(wₑ=0.093, wᵢ=0.167, noise=0.)


# Stability range for weights with noise
m = wload(datadir("stability", "network", "sum","e0=0_e1=0.2_i0=0_i1=0.2_noise=0.5_seed=2020_step=0.001.csv")) |> DataFrame
m = m[0.05 .< m.exc .< 0.13, :]
scatter_w_range(m, "Stability range for weights with noise")

# Weird weights in critical range:
inspect_weights(wₑ=0.06, wᵢ=0.054, noise=0., long=true)
inspect_weights(wₑ=0.087, wᵢ=0.162, noise=0., long=true)
inspect_weights(wₑ=0.048, wᵢ=0.051, noise=0., long=false)
inspect_weights(wₑ=0.049, wᵢ=0.193, noise=0., long=true)


# Stability range for fp weights with noise
m = wload(datadir("stability", "fixed_points", "sum", "fp_e0=0_e1=0.2_i0=0_i1=0.2_seed=2020_step=0.001.csv")) |> DataFrame
scatter_w_range(m, "Stability range for fp weights with noise")

# Right of step (0 inhibition)
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0., noise=0.5e-3, fpn=1, seed=2020)

# Conjuntion of step with rest
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0.1, noise=0.5e-3, fpn=1, seed=2020)

# Left end of the step (max inhibition)
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0.2, noise=0.5e-3, fpn=1, seed=2020)

# Highest excitation, lowest inhibition
inspect_weights(wₑᶠ=0.2, wᵢᶠ=0.0, noise=0.5e-3, fpn=1, seed=2020)

# Critical zone
inspect_weights(wₑᶠ=0.055, wᵢᶠ=0.005, noise=0.5e-3, fpn=1, seed=2020)
