using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Statistics
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))


function find_stable_w(e_range, i_range, noise=0., seed=0)
	stability_matrix = DataFrame(exc=Float64[], inh=Float64[], sum=Int64[])
	l = ReentrantLock() # create lock variable

	for i in i_range
		@show i	
		Threads.@threads for e in e_range

			ring = Ring(wₑ=e, wᵢ=i, noise=noise, seed=seed)
			ring()
			s = sum(ring.S)

			lock(l)
			push!(stability_matrix, (e, i, s))
			unlock(l)
		end
	end
	stability_matrix
end


function find_stable_fp_w(e_range, i_range, fps=[32], seed=seed)
	stability_matrix = DataFrame(exc=Float64[], inh=Float64[], sum=Int64[])
	l = ReentrantLock() # create lock variable

	for i in i_range
		@show i
		Threads.@threads for e in e_range

			ring = Ring(wₑᶠ=e, wᵢᶠ=i, fps=fps)
			ring()
			s = sum(ring.S)

			lock(l)
			push!(stability_matrix, (e, i, s))
			unlock(l)
		end
	end
	stability_matrix
end

