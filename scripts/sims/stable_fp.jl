using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
include(srcdir("ring-attractor.jl"))

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


e0 = 0.00
e1 = 0.20
i0 = 0.00
i1 = 0.2
step = 0.001
seed=2020

r_e = e0:step:e1
r_i = i0:step:i1


m = find_stable_fp_w(r_e, r_i, [32], seed, true)
tmp = @dict e0 e1 i0 i1 step seed
safesave(datadir("stability", "fixed_points", "sum", savename("fp", tmp, "csv")), m)
