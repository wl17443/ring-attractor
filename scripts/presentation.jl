using DrWatson
@quickactivate "Ring Attractor"

using Plots
using Statistics
using DataFrames
using StatsPlots
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))

##
r1 = Ring(N=1, time=60, noise=0)
r1()
r4 = Ring(N=4, time=60, noise=0)
r4()
r6 = Ring(N=6, time=60, noise=0)
r6()

plotlyjs()
plot([r1.V[1, :], r4.V[1, :], r6.V[1, :]], lw=1.5, 
     label=["Single Neuron" "Coupled Neurons" "Six Neurons"],
     size=(700,450))
xaxis!("Time (ms)")
yaxis!("Voltage (V)")
##


##
gr()
ring = Ring(N=48)
plot(showaxis=false, size=(600, 550), colorbar=:none, 
     heatmap(ring.Wₑ, colorbar=:none, c=[:grey4, :red4], 
             yaxis=("Receiving Neurons", (1:64), []), 
             xaxis=("Emitting Neurons", (1:64), []),
             title="Excitatory connections"),
     heatmap(ring.Wₑ, proj=:polar, c=[:grey4, :red4]),
     heatmap(ring.Wᵢ, colorbar=:none, c=[:grey4, :blue3], 
             yaxis=("Receiving Neurons", (1:64), []), 
             xaxis=("Emitting Neurons", (1:64), []),
             title="Inhibitory connections"),
     heatmap(ring.Wᵢ, proj=:polar, c=[:grey4, :blue3]))
##

##
ring = Ring(N=32, noise=0, time=200)
ring()
heatmap(ring.V, colorbar_title="Voltage (V)", size=(700, 450))
xaxis!("Time (ms)")
yaxis!("Neuron #")

ring = Ring(N=64, noise=8e-4, time=10000, seed=44)
ring()
heatmap(ring.V, colorbar_title="Voltage (V)", size=(700, 450))
xaxis!("Time (ms)")
yaxis!("Neuron #")
##

##
noises = [0:1e-5:10e-4;]
fprange = [0, [2^n for n in 1:3]...]
iters = 5

errors = DataFrame(fixed_points=Int[], noise=Float64[], error_mean=Float64[], error_var=Float64[], iter=Int[])
for it in 1:iters
    for fpn in fprange
        for noise in noises
            ring = Ring(noise=noise, fpn=fpn)
            e = sim_and_measure(ring)
            push!(errors, (fpn, noise, e[1], e[2], it))
        end
    end
end

plotlyjs()
fp0 = groupby(errors, :fixed_points)[1]
@df fp0 scatter(:noise, :fixed_points, :error_mean, size=(800,800))
##

##
fp0 = groupby(errors, :fixed_points)[1]
fp2 = groupby(errors, :fixed_points)[2]
fp4 = groupby(errors, :fixed_points)[3]
fp8 = groupby(errors, :fixed_points)[4]

@df fp8 scatter(:noise, :fixed_points, :error_mean, size=(800,800),
    xaxis=("Noise"), yaxis=("Fixed Points"), zaxis=("Error"), lab="Fixed Points=8" )
@df fp4 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=2" )
@df fp2 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=4" )
@df fp0 scatter!(:noise, :fixed_points, :error_mean, size=(800,800), lab="Fixed Points=0" )
##

##
@df fp8 scatter(:noise, :error_mean, size=(800,800),
    xaxis=("Noise"), yaxis=("Error"), lab="Fixed Points=8" )
@df fp4 scatter!(:noise, :error_mean, size=(800,800), lab="Fixed Points=2" )
@df fp2 scatter!(:noise, :error_mean, size=(800,800), lab="Fixed Points=4" )
@df fp0 scatter!(:noise, :error_mean, size=(800,800), lab="Fixed Points=0" )
##

##
@df fp8 plot(:noise, :error_mean, size=(800,800),
    xaxis=("plotse"), yaxis=("Fixed Points"), zaxis=("Error"), lab="Fixed Points=8" )
@df fp4 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=2" )
@df fp2 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=4" )
@df fp0 plot!(:noise, :error_mean, size=(800,800), lab="Fixed Points=0" )
##