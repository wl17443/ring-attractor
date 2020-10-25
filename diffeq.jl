using DifferentialEquations

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

const n_exc = 5
const n_inh = 7
const fp_width = 2


mutable struct Network <: Function
	N::Int32
	time::Int32
	noise::Float64
	fps::Tuple
	seed::Int32

	Wi::Array{Float64, 2}
	We::Array{Float64, 2}

	v::Array{Float64, 1}
	sd::Array{Float64, 2}
	t::Int32

	function Network(;N=64, time=10000, noise=5e-4, fps=(), seed=0, w_exc=0.05, w_inh=0.10, w_exc_fp=0.05, w_inh_fp=0.25)
		self = new()

		self.N = N
		self.time = time
		self.noise = noise
		self.fps = fps
		self.seed = seed

		self.We, self.Wi = genweights(N, fps, [w_exc, w_inh, w_exc_fp, w_inh_fp] .* kₛ * 1e-6 / Cₘ)

		self.sd = fill(0.2, self.N, 3)
		self.t = 0

		return self
	end
end

function genweights(N, fps, w)
    W = reshape(Float64[min(N - abs(i-k), abs(i-k)) for i in 1:N for k in 1:N], (N,N))

	We = deepcopy(W)
	replace!(x -> 0., view(We, We .> n_exc))
	replace!(x -> w[1], view(We, We .> 0.))

	Wi = deepcopy(W)
	replace!(x -> 0., view(Wi, n_exc .>= Wi))
	replace!(x -> 0., view(Wi, Wi .> n_exc + n_inh))
	replace!(x -> w[2],  view(Wi, Wi .> 0.))

    for fp in fps
		r = (fp:fp + 2) .- 1
		replace!(view(We, r, :), w[1] => w[3])
		replace!(view(Wi, r, :), w[2] => w[4])
    end

    return We, Wi
end

function (net::Network)(du, u, p, t)
	net.t += 1
	idx = net.t % 3 + 1
	s, k, We, Wi = p

	s .= (u .== 0.)

	@. k = @views net.sd[:, idx] * exp(-net.sd[:, idx] / τₛ)
	We .= net.We' * k
	Wi .= net.Wi' * k

	@. du = (Eₗₜ - u / τₘ ) - (u.-Eₑ) * We - (u.-Eᵢ) * Wi

	u[s] .= Vᵣ
	u[u .>= Vₜ] .= 0.
	du[s] .= Vᵣ
	du[u .>= Vₜ] .= 0.

	net.sd .+= dt
	net.sd[s, idx] .= 0.

end


p = falses(64), zeros(64), zeros(64), zeros(64) #Those can also be defined outside
v = fill(Vᵣ, 64)
v[30:35] .= 0.

function simulate(p, v)
	net = Network()

	alg = FunctionMap{true}()
	prob = DiscreteProblem(net, v, (dt, net.time*dt), p)
	sol= solve(prob, alg, dt=dt, saveat=dt)

	# spikes =  Array{Int, 2}(a .== 0)
	# pot = Array(sol)
	sol
end

sol = simulate(p, v)
