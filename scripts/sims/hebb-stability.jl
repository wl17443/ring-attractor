@everywhere using DrWatson
@quickactivate "Ring Attractor"

@everywhere using Printf

function include_everywhere(filepath)
    fullpath = joinpath(@__DIR__, filepath)
    @sync for p in procs()
        @async remotecall_wait(include, p, fullpath)
    end
end

include_everywhere("src/hebb.jl")

hebb_range = [5e-10:1e-8:5e-6;]
noise_range = [0.0:4e-6:2e-3;]
seed=2020

d = dict_list(Dict("hebb"=>hebb_range,
				   "noise"=>noise_range,
				   "seed"=>seed,
				   "sᵢ"=>0,
				   "sₒ"=>0))

@everywhere function f(par)
	idx_in = 27:37
	idx_out = setdiff(1:62, 27:37)

	hring = HebbRing()
	hring(ϵ=par["noise"], η=par["hebb"], seed=par["seed"])

	par["sᵢ"] = sum(hring.S[idx_in, :])
	par["sₒ"] = sum(hring.S[idx_out, :])

	ϵ = @sprintf("%.2e", par["noise"])
	η = @sprintf("%.2e", par["hebb"])
	sname = savename((@dict ϵ η), "bson")
"1.000E+10"                         
	safesave(datadir("results", sname), par)
end
