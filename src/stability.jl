using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Statistics
include(srcdir("ring-attractor.jl"))
include(srcdir("hebb.jl"))
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


function find_stable_fp_w(e_range, i_range, fps=[32], seed=seed, restrained=true)
	stability_matrix = DataFrame(exc=Float64[], inh=Float64[], sum=Int64[])
	l = ReentrantLock() # create lock variable

	for i in i_range
		@show i
		Threads.@threads for e in e_range

			ring = Ring(wₑᶠ=e, wᵢᶠ=i, fps=fps)
			ring()
			if restrained
				s = sum(ring.S[30:34, :])
			else
				s = sum(ring.S)
			end


			lock(l)
			push!(stability_matrix, (e, i, s))
			unlock(l)
		end
	end
	stability_matrix
end


function noise_vs_hebb(hebb_range, noise_range, seed=seed)
	count_inside = DataFrame(noise=Float64[], hebb=Float64[], sum_inside=Int64[], sum_outside=Int64[])
	l = ReentrantLock() # create lock variable

	for h in hebb_range
		@show h
		Threads.@threads for n in noise_range

			hring = HebbRing(noise=n, hebb=h, seed=seed)
			hring()

			minus(indx, x) = setdiff(1:length(x), indx)
			sᵢ = sum(hring.S[27:37, :])
			sₒ = sum(hring.S[setdiff(1:62, 27:37), :])


			lock(l)
			push!(count_inside, (n, h, sᵢ, sₒ))
			unlock(l)
		end
	end
	count_inside
end
