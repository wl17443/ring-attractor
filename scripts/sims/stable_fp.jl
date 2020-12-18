@everywhere using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
@everywhere using Printf
include(srcdir("utils.jl"))
include_everywhere("../src/hebb.jl")


exc_range = inh_range = [0.0:0.001:0.2;]

seed=2020

@printf("[*] Starting simulation...")

d = dict_list(Dict("e"=>exc_range,
				   "i"=>inh_range,
				   "seed"=>seed,
				   "count_inside"=>0,
				   "count_outside"=>0));

@printf("[*] %d parameters combinations found...", length(d))

@everywhere function f(par)
	idx_in = 27:37
	idx_out = setdiff(1:62, 27:37)

	hring = HebbRing(wₑᶠ=par["e"], wᵢᶠ=par["i"])
	hring(seed=par["seed"], fps=[32], ϵ=2.5e-3)

	par["count_inside"] = sum(hring.S[idx_in, :])
	par["count_outside"] = sum(hring.S[idx_out, :])

	e = par["e"]
	i = par["i"]
	sname = savename((@dict e i), "bson")
	safesave(datadir("stability", "fixed-points-with-noise", sname), par)
end

pmap(f, d)
