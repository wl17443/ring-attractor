using DrWatson
@quickactivate "Ring Attractor"

using Distributions
using Combinatorics
using Random

include(srcdir("utils.jl"))

const ms = 1e-3
const mV = 1e-3
const nF = 1e-9
const dt = 1e-3

const Vₜ = -48 * mV
const Vᵣ = -80 * mV
const Cₘ = 1e-9
const Eᵢ = -70 * mV
const Eₑ = 0.
const Eₘ = -70 * mV
const Eₗ = -70 * mV
const τᵣ = 2 * ms
const τₛ = 5 * ms
const τₘ = 5 * ms
const kₛ = 1/(5 * ms * exp(-1.))
const Eₗₜ = Eₗ/τₛ

const Nₑ = 5
const Nᵢ = 7
const fp_w = 2


"""
	HebbRing([N, time, wₑ, wᵢ, wₑᶠ, wᵢᶠ, τᵣ])

Create the network preallocating all the arrays

# Arguments
- `N::Int=64`: number of neurons in the network
- `time::Int=10000`: time of simulation (in milliseconds)
- `wₑ::Float64=0.05`: excitatory weight
- `wᵢ::Float64=0.10`: inhibitory weight
- `wₑᶠ::Float64=0.05`: excitatory weight for fixed points  
- `wᵢᶠ::Float64=0.25`: inhibitory weight for fixed points
- `τᵣ::Int=3`: refractory period (in milliseconds)
"""
mutable struct HebbRing <: Function
	N::Int32
	time::Int32
	t::Int32

	wₑ::Float64
	wᵢ::Float64
	wₑᶠ::Float64
	wᵢᶠ::Float64
	W::WeightMatrix


	S::Array{Bool, 2}
	V::Array{Float64, 2}
	Z::Array{Float64, 2}

	Δs::Array{Float64, 2}
	idx::CircularIndex
	k::Array{Float64, 1}


	function HebbRing(;N=64, time=10000, wₑ=0.05, wᵢ=0.10, wₑᶠ=0.05, wᵢᶠ=0.25, τᵣ=3)
		self = new()

		self.N = N
		self.time = time
		self.wₑ = wₑ
		self.wᵢ = wᵢ
		self.wₑᶠ = wₑᶠ
		self.wᵢᶠ = wᵢᶠ
		self.W = WeightMatrix()

		self.V = zeros(N, time)
		self.Z = zeros(N, time)
		self.S = falses(N, time)
		self.Δs = zeros(N, τᵣ)
		self.idx = CircularIndex(0, τᵣ)
		self.k = zeros(N)
		self.t = 0

		return self
	end
end


"""
	HebbRing([α, ϵ, η, fps, fpn, resetW, seed])

Simulate the network

# Arguments
- `α::Int=32`: center of the stimulation
- `ϵ::Float64=5e-4`: noise
- `η::Float64=0.`: learning coefficient
- `fps::Tuple=()`: indexes of fixed points (overrides fpn)
- `fpn::Int=0`: number of fixed points
- `resetW::Int=1`: if 0: don't reset, if 1: reset only if η > 0, if 2: force reset
- `seed::Int=1`: random seed
"""
function (r::HebbRing)(;α=32, ϵ=5e-4, η=0., fps=(), fpn=0, resetW=1, seed=0)
	init!(r, α, ϵ, η, fps, fpn, resetW, seed)

	for r.t = 1:r.time-1
		# Go forth one time step
		++(r.idx)

		# Update spikes
		r.S[:, r.t] .= view(r.V, :, r.t) .== 0.

		# Update weights
		if η != 0.
			for (i, j) = combinations(findall(view(r.S, :, r.t) .> 0), 2)		
				@inbounds r.W[i, j] += η
			end
		end

		# Calculate variable that will be reused
		r.k .= @views r.Δs[:, r.idx.val] .* exp.(-r.Δs[:, r.idx.val] ./ τₛ) .* (kₛ * 1e-6 / Cₘ)

		# Caluculate voltage update
		r.V[:, r.t+1] .= @views r.V[:, r.t] .+ ((Eₗₜ .- r.V[:, r.t] ./ τₘ ) .- (r.V[:, r.t].-Eₑ) .* (r.W.e' * r.k) .- (r.V[:, r.t].-Eᵢ) .* (r.W.i' * r.k)) .* dt
		r.V[:, r.t+1] .+= @view r.Z[:, r.t+1]

		# Make neurons spike
		r.V[view(r.V,:, r.t) .> Vₜ, r.t+1] .= 0.

		# Reset neurons that spiked the time step before
		r.V[view(r.S, :, r.t), r.t+1] .= Vᵣ

		# Go forth one time step in the spike delays
		r.Δs .+= dt

		# Reset spike delays of neurons that spiked
		r.Δs[view(r.S, :, r.t), r.idx.val] .= 0.
	end
end

"""
	init!(r, α, ϵ, η, fps, fpn, resetW, seed)

Initialize the network

# Arguments
- `r::HebbRing`: network to initialize
- `α::Int=32`: center of the stimulation
- `ϵ::Float64=5e-4`: noise
- `η::Float64=0.`: learning coefficient
- `fps::Tuple=()`: indexes of fixed points (overrides fpn)
- `fpn::Int=0`: number of fixed points
- `resetW::Int=1`: if 0: don't reset, if 1: reset only if η > 0, if 2: force reset
- `seed::Int=1`: random seed
"""
function init!(r::HebbRing, α, ϵ, η, fps, fpn, resetW, seed)
	# Get fixed points
	fps = length(fps) == 0 ? get_fixed_points(r.N, fpn) : fps

	# Set seed
	if seed != 0
		Random.seed!(seed)
	end
	# Reset weights
	if r.t == 0 || resetW == 2 || resetW == 1 && η > 0.
		r.W = WeightMatrix(r.N, r.wₑ, r.wᵢ, r.wₑᶠ, r.wᵢᶠ, Nₑ, Nᵢ, fps)
	end

	# Reset time
	r.t = 0

	# Reset index
	r.idx.val = 0

	# No synaptic currents at the beginning
	fill!(r.Δs, 0.2)

	# Assign noise
	r.Z .= rand(Normal(0., ϵ), r.N, r.time)

	# Reset membrane potential
	replace!(view(r.V, :, 1), 0. => Vᵣ)

	# Force spikes as stimulation
	replace!(view(r.V, (α-2:α+3), 1), Vᵣ => 0.)
end
