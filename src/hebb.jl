using DrWatson
@quickactivate "Ring Attractor"

using Distributions
using Combinatorics
using Random

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


mutable struct CircularIndex
       val::Int
       per::Int
end

function ++(x::CircularIndex)
       x.val = x.val % x.per + 1
end

mutable struct HebbRing <: Function
	N::Int32
	time::Int32
	t::Int32

	wₑ::Float64
	wᵢ::Float64
	wₑᶠ::Float64
	wᵢᶠ::Float64
	Wₑ::Array{Float64, 2}
	Wᵢ::Array{Float64, 2}


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

		self.Wₑ = zeros(N, N)
		self.Wᵢ = zeros(N, N)
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


# hebb, noise, resetWeights, stim_pos, 
"""
	α: center of the stimulation
	ϵ: noise
	η: learning coefficient
	fpn: number of fixed points
	fps: indexes of fixed points (overrides fpn)
	resetW: if 0: don't reset, if 1: reset only if η > 0, if 2: force reset
	seed: random seed
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
				@inbounds r.Wᵢ[i, j] += η
				@inbounds r.Wᵢ[j, i] += η

				@inbounds r.Wₑ[i, j] += η
				@inbounds r.Wₑ[j, i] += η
			end
		end

		# Calculate variable that will be reused
		r.k .= @views r.Δs[:, r.idx.val] .* exp.(-r.Δs[:, r.idx.val] ./ τₛ) .* (kₛ * 1e-6 / Cₘ)

		# Caluculate voltage update
		r.V[:, r.t+1] .= @views r.V[:, r.t] .+ ((Eₗₜ .- r.V[:, r.t] ./ τₘ ) .- (r.V[:, r.t].-Eₑ) .* (r.Wₑ' * r.k) .- (r.V[:, r.t].-Eᵢ) .* (r.Wᵢ' * r.k)) .* dt
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


function setweights!(r::HebbRing, fps)
	r.Wₑ .= reshape(Float64[min(r.N - abs(i-k), abs(i-k)) for i in 1:r.N for k in 1:r.N], (r.N,r.N))
	r.Wᵢ .= deepcopy(r.Wₑ)

	replace!(x -> 0., view(r.Wₑ, r.Wₑ .> Nₑ))
	replace!(x -> r.wₑ, view(r.Wₑ, r.Wₑ .> 0.))

	replace!(x -> 0., view(r.Wᵢ, Nₑ .>= r.Wᵢ))
	replace!(x -> 0., view(r.Wᵢ, r.Wᵢ .> Nₑ + Nᵢ))
	replace!(x -> r.wᵢ,  view(r.Wᵢ, r.Wᵢ .> 0.))

    for fp in fps
		replace!(view(r.Wₑ, (fp:fp+2).-1, :), r.wₑ => r.wₑᶠ)
		replace!(view(r.Wᵢ, (fp:fp+2).-1, :), r.wᵢ => r.wᵢᶠ)
    end
end

function init!(r::HebbRing, α, ϵ, η, fps, fpn, resetW, seed)
	# Set seed
	if seed != 0
		Random.seed!(seed)
	end

	# No synaptic currents at the beginning
	fill!(r.Δs, 0.2)

	# Reset index
	r.idx.val = 0

	# Assign noise
	r.Z .= rand(Normal(0., ϵ), r.N, r.time)

	# Reset membrane potential
	replace!(view(r.V, :, 1), 0. => Vᵣ)

	# Force spikes as stimulation
	replace!(view(r.V, (α-2:α+3), 1), Vᵣ => 0.)

	# Reset weights
	if r.Wₑ == r.Wᵢ || resetW == 2 || resetW == 1 && η > 0.
		fps = length(fps) == 0 ? get_fixed_points(r.N, fpn) : fps
		setweights!(r, fps)
	end
end

function get_fixed_points(N, fpn)::Array{Int64, 1}
	if fpn == 0
		return []
	end

	findall([1:1:N;] .% (N ÷ fpn) .== 0) .- N ÷ fpn ÷ 2
end


