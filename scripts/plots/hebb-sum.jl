using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Plots; gr()
using StatsPlots
using Statistics


include(srcdir("utils.jl"))
df = wload(datadir("hebb", "results_noise_vs_hebb.bson"))[:df]
gdf = groupby(df, :noise)
comb = combine(gdf, :sₒ => mean, :sᵢ => mean)

@df comb scatter(:noise, :sᵢ_mean, size=(800, 800), title="Mean sum of spikes by noise", xaxis="Noise", yaxis="Sum of spikes", lab="Spikes inside stimulation region")
@df comb scatter!(:noise, :sₒ_mean, lab="Spikes outside stimulation region", legend=:right)

gdf = groupby(df, :hebb)
comb = combine(gdf, :sₒ => mean, :sᵢ => mean)

@df comb scatter(:hebb, :sᵢ_mean, size=(800, 800), title="Mean sum of spikes by learning rate", xaxis="Learning rate", yaxis="Sum of spikes", lab="Spikes inside stimulation region", markerstrokewidth = 0., markerstrokecolor=:blue, markerstrokealpha=0.)
@df comb scatter!(:hebb, :sₒ_mean, lab="Spikes outside stimulation region", legend=:left, markerstrokewidth = 0., markerstrokecolor=:orange)
