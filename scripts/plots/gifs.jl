using DrWatson
@quickactivate "Ring Attractor"

using Plots
using Statistics
using DataFrames
using StatsPlots
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))

function partial_filter(S, N, bin=100, step=1)
    spikes = convert(Array{Float64, 2}, S)
    spikes .*= [1:1:N;]
	normes = zeros(Float64, (size(S, 2) ÷ step))

	for (k, i) in enumerate(1:step:size(spikes, 2) - 2bin)
        s1_var, s1_mean, s1_fit = slide_measures(view(spikes, :, i:i+bin))
        s2_var, s2_mean, s2_fit = slide_measures(view(spikes, :, i+bin:i+2bin))
        normes[k] = norm([abs(s1_var - s2_var), abs(s1_mean - s2_mean), kl_divergence(s1_fit, s2_fit)])
    end
    normes
end
ring = Ring(noise=0)
ring()
anim = @animate for i in 1:200
	heatmap(ring.V[:, 1:i]', proj=:polar, cbar=:none, yaxis=("", (1:i), []))
end
gif(anim, "stable.gif", fps = 30)

##
gr()
ring = Ring(noise=2.5e-3, seed=51)
ring()
anim = @animate for i in 1:200:10000
	l = @layout [ a{0.6h}
				  b 
				  c{0.6w} d ]
	p1 = heatmap(ring.V[:, 1:i]', proj=:polar, cbar=:none, yaxis=("", (1:i), []))
	p2 = heatmap(ring.V[:, 1:i], cbar=:none, xaxis="Time (ms)")
	p3 = plot(partial_filter(ring.S[:, 1:i], ring.N), lw=2, yaxis="Error")
	p4 = bar([[0, mean(partial_filter(ring.S[:, 1:i], ring.N))], [std(partial_filter(ring.S[:, 1:i], ring.N))]], lab=["Error mean" "Error std"], yaxis=("", (0,1), [0:0.1:1;]))
	plot(p1, p2, p3, p4, layout=l, size=(800,1000))
end
gif(anim, "unstable_circ.gif", fps = 20)
##
#
anim = @animate for i in 2:100:10000
	l = @layout [ a{0.6h} 
				  b 
				  c{0.6w} d ]
	p1 = heatmap(ring.V[:, 1:i], cbar=:none)
	p2 = bar(sum(ring.S[:, 1:i], dims=2), yaxis="# of spikes" )
	p3 = plot(partial_filter(ring.S[:, 1:i], ring.N), lw=2, yaxis=" Inst. Error")
	p4 = bar([[0, mean(partial_filter(ring.S[:, 1:i], ring.N))], [std(partial_filter(ring.S[:, 1:i], ring.N))]], lab=["Error mean" "Error std"], xaxis=("", (0.5, 2.5), []), yaxis=("", (0,.5), [0:0.1:.5;]))
	plot(p1, p2, p3, p4, layout=l, size=(800,1000))
end
gif(anim, "unstable.gif", fps = 20)


ring = Ring(noise=2.5e-3, seed=51, fpn=4)
ring()
anim = @animate for i in 2:100:10000
	l = @layout [ a{0.6h} 
				  b 
				  c{0.6w} d ]
	p1 = heatmap(ring.V[:, 1:i], cbar=:none)
	p2 = bar(sum(ring.S[:, 1:i], dims=2), yaxis="# of spikes" )
	p3 = plot(partial_filter(ring.S[:, 1:i], ring.N), lw=2, yaxis=" Inst. Error")
	p4 = bar([[0, mean(partial_filter(ring.S[:, 1:i], ring.N))], [std(partial_filter(ring.S[:, 1:i], ring.N))]], lab=["Error mean" "Error std"], xaxis=("", (0.5, 2.5), []), yaxis=("", (0,.5), [0:0.1:.5;]))
	plot(p1, p2, p3, p4, layout=l, size=(800,1000))
end
gif(anim, "unstable-w_fp.gif", fps = 20)
