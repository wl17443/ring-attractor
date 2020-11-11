using DrWatson
@quickactivate "Ring Attractor"

include(srcdir("plots.jl"))
using CSV

# Load data from python simulations
python_errors = CSV.read(datadir("biasvariance", "batch_4", "means.csv")) |> DataFrame
python_errors = stack(python_errors)
names!(python_errors, [:fixed_points, :noise, :error_mean])
python_errors.noise = map(x->parse(Float64,String(x)),python_errors.noise)

## Reproduce lineplot
plot_biasvariance(python_errors)

# Reproduce scatterplot
scatter_biasvariance(python_errors)