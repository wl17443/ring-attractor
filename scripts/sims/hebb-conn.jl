@everywhere using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
@everywhere using Printf
include(srcdir("utils.jl"))
include_everywhere("../src/hebb.jl")

hebb_range = [5e-10:5e-7:5e-6;];
noise_range = [0.0:2e-4:2e-3;];

seed=2020

@printf("[*] Starting simulation...")

d = dict_list(Dict("hebb"=>hebb_range,
				   "noise"=>noise_range,
				   "seed"=>seed,
				   "W"=>zeros(64, 64)));

@printf("[*] %d parameters combinations found...", length(d))

@everywhere function f(par)
	hring = HebbRing()
	hring(ϵ=par["noise"], η=par["hebb"], seed=par["seed"])

	par["W"] = hring.W.W

	ϵ = @sprintf("%.4e", par["noise"])
	η = @sprintf("%.4e", par["hebb"])
	sname = savename((@dict ϵ η), "bson")
	safesave(datadir("hebb", "weight-matrix", sname), par)
end

@time pmap(f, d)

df = collect_results!(datadir("hebb", "weight-matrix"))
