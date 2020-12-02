@everywhere using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
@everywhere using Printf
include(srcdir("utils.jl"))
include_everywhere("../../src/hebb.jl")

hebb_range = [5e-10:5e-9:5e-6;];
noise_range = [0.0:2e-6:2e-3;];

length(hebb_range)
length(noise_range)
seed=2020

@printf("[*] Starting simulation...")

d = dict_list(Dict("hebb"=>hebb_range,
				   "noise"=>noise_range,
				   "seed"=>seed,
				   "sᵢ"=>0,
				   "sₒ"=>0));

@printf("[*] %d parameters combinations found...", length(d))

@everywhere function f(par)
	idx_in = 27:37
	idx_out = setdiff(1:62, 27:37)

	hring = HebbRing()
	hring(ϵ=par["noise"], η=par["hebb"], seed=par["seed"])

	par["sᵢ"] = sum(hring.S[idx_in, :])
	par["sₒ"] = sum(hring.S[idx_out, :])

	ϵ = @sprintf("%.4e", par["noise"])
	η = @sprintf("%.4e", par["hebb"])
	sname = savename((@dict ϵ η), "bson")
	safesave(datadir("hebb", sname), par)
end

@time pmap(f, d)

df = collect_results!(datadir("hebb"))
