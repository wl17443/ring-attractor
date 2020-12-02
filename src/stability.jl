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


struct R2AEnumerate{S,T}
    itra::S
    itrb::T
end
Base.eltype(r::R2AEnumerate) = Tuple{Int,eltype(r.itra),eltype(r.itrb)}
Base.length(r::R2AEnumerate) = length(a)*length(b)
Base.firstindex(r::R2AEnumerate) = 1
Base.lastindex(r::R2AEnumerate) = length(a)*length(b)
Base.getindex(r::R2AEnumerate, i) = (i, r.itra[i%length(a)+1], r.itrb[(i-1)÷length(a)+1])



function noise_vs_hebb(hebb_range, noise_range, seed=seed)
	data = zeros(length(hebb_range) * length(noise_range), 4)

	idx_in = 27:37
	idx_out = setdiff(1:62, 27:37)

	hring = HebbRing()
	@inbounds for (i, h) in enumerate(hebb_range)
		@inbounds for (j, n) in enumerate(noise_range)

			hring(ϵ=n, η=h, seed=seed)

			sᵢ = sum(hring.S[idx_in, :])
			sₒ = sum(hring.S[idx_out, :])

			data[j + (i - 1) * length(hebb_range), :] .= [n, h, sᵢ, sₒ]
		end
	end
	DataFrame(data, [:noise, :hebb, :sum_inside, :sum_outside])
end


function paral_noise_vs_hebb(hebb_range, noise_range, seed=seed)
	data = zeros(length(hebb_range) * length(noise_range), 4)

	idx_in = 27:37
	idx_out = setdiff(1:62, 27:37)

	Threads.@threads for h in hebb_range
		hring = HebbRing()
		@inbounds for (j, n) in enumerate(noise_range)

			hring(ϵ=n, η=h, seed=seed)

			sᵢ = sum(hring.S[idx_in, :])
			sₒ = sum(hring.S[idx_out, :])

			data[j + 1* length(hebb_range), :] .= [n, h, sᵢ, sₒ]
		end
	end
	DataFrame(data, [:noise, :hebb, :sum_inside, :sum_outside])
end


