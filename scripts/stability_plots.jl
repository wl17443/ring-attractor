using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()
using StatsPlots
using DataFrames 

include(srcdir("plots.jl"))

# Stability range for weights with no noise

m = wload("data/stability/e0=0.01_e1=0.2_i0=0.05_i1=0.2_iters=1_noise=0_step=0.001.csv") |> DataFrame
m = m[0.05 .< m.exc .< 0.13, :]
scatter_w_range(m)

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



m1 = wload("data/stability/fp_e0=0.01_e1=0.2_i0=0_i1=0.049_iters=1_noise=0.5_step=0.001.csv") |> DataFrame
m2 = wload("data/stability/fp_e0=0.01_e1=0.2_i0=0.05_i1=0.2_iters=1_noise=0.5_step=0.001.csv") |> DataFrame
mfull = outerjoin(m1, m2, on=[:exc, :inh, :sum])
scatter_w_range(mfull)

# Right of step (0 inhibition)
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0., noise=0.5e-3, fpn=1)

# Conjuntion of step with rest
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0.1, noise=0.5e-3, fpn=1)

# Left end of the step (max inhibition)
inspect_weights(wₑᶠ=0.05, wᵢᶠ=0.2, noise=0.5e-3, fpn=1)

# Highest excitation, lowest inhibition
inspect_weights(wₑᶠ=0.2, wᵢᶠ=0.0, noise=0.5e-3, fpn=1)

# Critical zone
inspect_weights(wₑ=0.05, wᵢ=0.05, noise=0.5e-3)
inspect_weights(wₑᶠ=0.073, wᵢᶠ=0.023, noise=0.5e-3, fpn=1)
inspect_weights(wₑᶠ=0.07, wᵢᶠ=0.03, noise=0.5e-3, fpn=1)
inspect_weights(wₑᶠ=0.062, wᵢᶠ=0.059, noise=0.5e-3, fpn=1)
inspect_weights(wₑᶠ=0.078, wᵢᶠ=0.003, noise=0.5e-3, fpn=1)


