using DrWatson
@quickactivate "Ring Attractor"

mutable struct CircularIndex
       val::Int
       per::Int
end

function ++(x::CircularIndex)
       x.val = x.val % x.per + 1
end

function include_everywhere(filepath)
    fullpath = joinpath(@__DIR__, filepath)
    @sync for p in procs()
        @async remotecall_wait(include, p, fullpath)
    end
end

function get_fixed_points(N, fpn)::Array{Int16, 1}
	if fpn == 0
		return []
	end

	findall([1:1:N;] .% (N ÷ fpn) .== 0) .- N ÷ fpn ÷ 2
end


struct WeightMatrix <: AbstractArray{Float64, 2}
	W::Array{Float64, 2}
	e::Array{Float64, 2}
	i::Array{Float64, 2}

	function WeightMatrix(N=64, wₑ=0.05, wᵢ=0.1, wₑᶠ=0.05, wᵢᶠ=0.20, Nₑ=5, Nᵢ=7, fps=())
		e = reshape(Float64[min(N - abs(i-k), abs(i-k)) for i in 1:N for k in 1:N], (N,N))
		i = deepcopy(e)

		replace!(x -> 0., view(e, e .> Nₑ))
		replace!(x -> wₑ, view(e, e .> 0.))

		replace!(x -> 0., view(i, Nₑ .>= i))
		replace!(x -> 0., view(i, i .> Nₑ + Nᵢ))
		replace!(x -> wᵢ,  view(i, i .> 0.))

		for fp in fps
			replace!(view(e, (fp:fp+2).-1, :), wₑ => wₑᶠ)
			replace!(view(i, (fp:fp+2).-1, :), wᵢ => wᵢᶠ)
		end

		W = e + i 
		self = new(W, e, i)
		return self
	end
end

Base.size(C::WeightMatrix) = (size(C.W))
Base.IndexStyle(::Type{<:WeightMatrix}) = IndexLinear()
Base.getindex(C::WeightMatrix, i::Int, j::Int) = C.W[i, j]

function Base.setindex!(C::WeightMatrix, v::Float64, i::Int, j::Int) 
	# No change of sign nor creation of new synapses allowed
	if (C.W[i, j] + v) * C.W[i, j] > 0
		if C.e[i, j] > 0
			C.e[i, j] = v
			C.e[j, i] = v

			C.W[i, j] = v
			C.W[j, i] = v
		elseif C.i[i, j] > 0
			C.i[i, j] = v
			C.i[j, i] = v

			C.W[i, j] = v
			C.W[j, i] = v
		end
	end
end

