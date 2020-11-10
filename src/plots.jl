using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()
using StatsPlots
using DataFrames 

function plot_stability_range(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	means = convert(Matrix, unstack(dropmissing(m), :exc, :inh, :means)[2:end])
 
	surface(exc, inh, means,
		colorbar_title="Error",
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis="Squared root of Mean Error")
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end

# > 0.8 inh, < 0.14 exc
#

function scatter_stability_range(m)
	@df m scatter(:exc, :inh, :means, markersize=1, size=(800,800))
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end

function plot_stability_range_v(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	means = convert(Matrix, unstack(m, :exc, :inh, :vars)[2:end])
 
	surface(exc, inh, means,
		colorbar_title="Error",
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis="Mean Error")
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end
