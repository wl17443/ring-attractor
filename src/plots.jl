using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()
using StatsPlots
using Plots.PlotMeasures
using DataFrames 
using Printf

function plot_stability_range(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	means = convert(Matrix, unstack(dropmissing(m), :inh, :exc, :means)[2:end])
 
	means ./= 5.
	surface(inh, exc, means,
		colorbar_title="Error",
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis="Mean Error",
		title="Stability of Fixed Points")
	yaxis!("Excitatory weights")
	xaxis!("Inhibitory weights")
end

function plot_w_range(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	sums = convert(Matrix, unstack(dropmissing(m), :inh, :exc, :sum)[2:end])
	sums[sums .< 10e3] .= -1
	sums[sums .> 50e3] .= 1
	sums[10e3 .<= sums .<= 50e3] .= 0
 
	surface(inh, exc, sums,
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis=("Stability", (-1., 1.), [-1, 0, 1]),
		title="Stability of weights")
	yaxis!("Excitatory weights")
	xaxis!("Inhibitory weights", (0., 0.2), [0.0:0.05:0.15;])
end

function scatter_stability_range(m)
	@df m scatter(:exc, :inh, :means, markersize=0.1, size=(800,800),
				  zaxis=("Mean Error"))
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end

function scatter_w_range(m)
	@df m scatter(:exc, :inh, :sum, markersize=0.1, size=(800,800),
				  zaxis=("# of spikes"), title="Stability of weights")
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end

function inspect_weights(;wₑ=0.05, wᵢ=0.1, wₑᶠ=0.05, wᵢᶠ=0.1, noise=0, fpn=0, long=false)
	ring = Ring(wₑ=wₑ, wᵢ=wᵢ, wₑᶠ=wₑᶠ, wᵢᶠ=wᵢᶠ, noise=noise, fpn=fpn)
	@show ring.wₑ, ring.wᵢ, ring.noise, ring.fpn, ring.fps
	ring()
	tit = @sprintf "wₑ=%.2f  wᵢ=%.2f  wₑᶠ=%.2f  wᵢᶠ=%.2f  noise=%.1e  fpn=%d" ring.wₑ ring.wᵢ ring.wₑᶠ ring.wᵢᶠ ring.noise ring.fpn
	l = 1000
	if long
		l *= 10
	end
	heatmap(ring.V, yaxis=("Neurons"), xaxis=("Time (ms)"), colorbar_title=("Voltage (V)"), size=(l, 640), title=tit, top_margin=10px)
end
