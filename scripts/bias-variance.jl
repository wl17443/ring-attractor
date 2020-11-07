using DrWatson
@quickactivate "Ring Attractor"

using Statistics
using DataFrames
using StatsPlots
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))

noises = [0:1e-5:10e-4;]
fprange = [0, [2^n for n in 1:3]...]
iters = 5

errors = DataFrame(fixed_points=Int[], noise=Float64[], error_mean=Float64[], error_var=Float64[])
for fpn in fprange
    for noise in noises
        ring = Ring(noise=noise, fpn=fpn)
        e = skipnan([sim_and_measure(ring) for _ in 1:iters])
        push!(errors, (fpn, noise, mean(e[1]), mean(e[2])))
    end
end


@df errors scatter(:noise, :fixed_points, :error_mean, size=(800,800))

fp0 = groupby(errors, :fixed_points)[1]
fp2 = groupby(errors, :fixed_points)[2]
fp4 = groupby(errors, :fixed_points)[3]
fp8 = groupby(errors, :fixed_points)[4]

@df fp8 scatter(:noise, :fixed_points, :error_mean, size=(800,800),
    xaxis=("Noise"), yaxis=("Fixed Points"), zaxis=("Errors") )
@df fp4 scatter!(:noise, :fixed_points, :error_mean, size=(800,800))
@df fp2 scatter!(:noise, :fixed_points, :error_mean, size=(800,800))
@df fp0 scatter!(:noise, :fixed_points, :error_mean, size=(800,800))