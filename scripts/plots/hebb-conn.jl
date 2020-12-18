using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Plots
using Printf
using StatsPlots
using Statistics

include(srcdir("utils.jl"))
df = collect_results!(datadir("hebb", "weight-matrix"))

Wstart = WeightMatrix().W

function inspect_weights(j)
	Wdiff = df[j, 1]
	title = @sprintf("Weight matrix with η=%.3e and ϵ=%.3e", df[j, 2], df[j, 4])
	heatmap(Wdiff, size=(1100,800), title=title, colorbar_title="Connection stenght")
	xaxis!("Neuron #")
	yaxis!("Neuron #")
end

function inspect_diff(j)
	Wdiff = df[j, 1] - Wstart
	title = @sprintf("Weight gained with η=%.3e and ϵ=%.3e", df[j, 2], df[j, 4])
	heatmap(Wdiff, size=(1100,800), title=title, colorbar_title="Difference from baseline")
	xaxis!("Neuron #")
	yaxis!("Neuron #")
end

gdf = groupby(df, :noise)
comb = combine(gdf, "W" => mean)
plot(comb[10, 2], linetype=:heatmap, title=@sprintf("Weight matrix with mean ϵ=%.3e", comb[10, 1]))

gdf = groupby(df, :hebb)
comb = combine(gdf, "W" => mean)
plot(comb[1, 2], linetype=:heatmap, title=@sprintf("Weight matrix with mean η=%.3e", comb[1, 1]))
