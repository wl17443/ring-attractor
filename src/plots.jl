using DrWatson
@quickactivate "Ring Attractor"

using Plots; plotlyjs()

function plot_stability_range(m)

	exc = m.exc
	inh = m.inh
	means = reshape(m.means ./ 5, (length(unique(exc)), length(unique(inh))))
 
	surface(exc, inh, means,
		colorbar_title="Error",
		size=(800, 800),
		c=:roma, # :viridis :batlow, :nuuk, :roma
		zaxis="Mean Error")
	xaxis!("Excitatory weights")
	yaxis!("Inhibitory weights")
end


