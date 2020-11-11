using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Statistics
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))


noises = [0:1e-5:10e-4;]
fprange = [0, [2^n for n in 1:3]...]
iters = 5

l = ReentrantLock() # create lock variable

errors = DataFrame(fixed_points=Int[], noise=Float64[], error_mean=Float64[], error_var=Float64[])
Threads.@threads for fpn in fprange
    for noise in noises
        ring = Ring(noise=noise, fpn=fpn)
        e = skipnan([sim_and_measure(ring) for _ in 1:iters])
		lock(l)
        push!(errors, (fpn, noise, mean(e[1]), mean(e[2])))
		unlock(l)
    end
end

# TODO add save