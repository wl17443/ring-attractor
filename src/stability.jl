using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Statistics
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))


function find_stable_w(e_range, i_range, noise=0., iters=7)
	stability_matrix = DataFrame(exc=Float64[], inh=Float64[], means=Float64[], vars=Float64[])
	l = ReentrantLock() # create lock variable

	for i in i_range
		@show i	
		Threads.@threads for e in e_range

			ring = Ring(wₑ=e, wᵢ=i, noise=noise)
			measures = [sim_and_measure(ring) for _ in 1:iters]
			m = mean(skipnan([i[1] for i in measures]))
			v = mean(skipnan([i[2] for i in measures]))

			lock(l)
			push!(stability_matrix, (e, i, m, v))
			unlock(l)
		end
	end
	stability_matrix
end


function find_stable_fp_w(e_range, i_range, fps=[32], iters=7)
	stability_matrix = DataFrame(exc=Float64[], inh=Float64[], means=Float64[], vars=Float64[])
	l = ReentrantLock() # create lock variable

	for i in i_range
		Threads.@threads for e in e_range

			ring = Ring(wₑᶠ=e, wᵢᶠ=i, fps=fps)
			measures = [sim_and_measure(ring) for _ in 1:iters]
			m = mean(skipnan([i[1] for i in measures]))
			v = mean(skipnan([i[2] for i in measures]))

			lock(l)
			push!(stability_matrix, (e, i, m, v))
			unlock(l)
		end
	end
	stability_matrix
end

