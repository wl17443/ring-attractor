using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
include(srcdir("ring-attractor.jl"))

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



e0 = 0.0
e1 = 0.2
i0 = 0.0
i1 = 0.2
step = 0.001
noise = 0.5e-3
seed = 2020

r_e = e0:step:e1
r_i = i0:step:i1

m = find_stable_w(r_e, r_i, noise, seed)
noise *= 1e3 
tmp = @dict e0 e1 i0 i1 step noise seed
safesave(datadir("stability", savename(tmp, "csv")), m)
