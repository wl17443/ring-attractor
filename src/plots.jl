using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()
using StatsPlots
using Plots.PlotMeasures
using DataFrames 
using Printf

include(srcdir("ring-attractor.jl"))

function plot_stability_range(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	means = convert(Matrix, unstack(dropmissing(m), :inh, :exc, :sum)[2:end])
 
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

function scatter_w_range(m, title="")
	@df m scatter(:exc, :inh, :sum, markersize=0.1, size=(800,800),
				  zaxis=("# of spikes"), title=title, label=false)
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end

function inspect_weights(;wₑ=0.05, wᵢ=0.1, wₑᶠ=0.05, wᵢᶠ=0.1, noise=0, fpn=0, long=false, seed=0)
	ring = Ring(wₑ=wₑ, wᵢ=wᵢ, wₑᶠ=wₑᶠ, wᵢᶠ=wᵢᶠ, noise=noise, fpn=fpn, seed=seed)
	ring()
	tit = @sprintf "wₑ=%.3f  wᵢ=%.3f  wₑᶠ=%.3f  wᵢᶠ=%.3f  noise=%.1e  fpn=%d" ring.wₑ ring.wᵢ ring.wₑᶠ ring.wᵢᶠ ring.noise ring.fpn
	l = 1000
	if long
		l *= 10
	end
	heatmap(ring.V, yaxis=("Neurons"), xaxis=("Time (ms)"), colorbar_title=("Voltage (V)"), size=(l, 640), title=tit, top_margin=10px)
end

function scatter_biasvariance(df)
	fp0 = groupby(df, :fixed_points)[1]
	fp1 = groupby(df, :fixed_points)[2]
	fp2 = groupby(df, :fixed_points)[3]
	fp4 = groupby(df, :fixed_points)[4]
	fp8 = groupby(df, :fixed_points)[5]
	fp16 = groupby(df, :fixed_points)[6]
	fp32 = groupby(df, :fixed_points)[7]

	p = @df fp32 scatter(:noise, :fixed_points, :error_mean, size=(800,800),
    xaxis=("Noise"), yaxis=("Fixed Points", (0,32), [0, 1, 2, 4, 16, 32]), zaxis=("Error"), lab="Fixed Points=32")
	p = @df fp16 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=16" )
	p = @df fp8 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=8" )
	p = @df fp4 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=4" )
	p = @df fp2 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=2" )
	p = @df fp1 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=1" )
	p = @df fp0 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=0" )
	plot(p)
end

function plot_biasvariance(df)
	fp0 = groupby(df, :fixed_points)[1]
	fp1 = groupby(df, :fixed_points)[2]
	fp2 = groupby(df, :fixed_points)[3]
	fp4 = groupby(df, :fixed_points)[4]
	fp8 = groupby(df, :fixed_points)[5]
	fp16 = groupby(df, :fixed_points)[6]
	fp32 = groupby(df, :fixed_points)[7]

	p = @df fp32 plot(:noise, :error_mean, size=(800,800), lab="Fixed Points=32")
	p = @df fp16 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=16" )
	p = @df fp8 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=8" )
	p = @df fp4 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=4" )
	p = @df fp2 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=2" )
	# p = @df fp1 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=1" )
	p = @df fp0 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=0" )
	plot(p,xaxis=("Noise"), yaxis="Error", lw=1.)
end
