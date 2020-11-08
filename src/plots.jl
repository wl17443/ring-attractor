using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()

function plot_stability_range(m)

	exc = unique(m.exc)
	inh = unique(m.inh)
	means = convert(Matrix, unstack(m, :exc, :inh, :means)[2:end]) ./ 5
 
	surface(exc, inh, means,
		colorbar_title="Error",
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis="Mean Error")
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end


