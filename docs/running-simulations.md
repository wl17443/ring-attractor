# Initializing the project

1. Clone the project
2. cd into it
3. open Julia
4. type `] add DrWatson`
5. type `@quickactivate "Ring Attractor"`
6. type `instantiate`

This will install all the needed modules in the project's environment.


# Creating a new simulation

1. Create a new file in scripts/sims/
2. As every file in the project, the first 2 lines are to import `DrWatson` and to activate the Julia environment (`@quickactivate "Ring Attractor"`)

> In case you want to run the code in parallel just prepend `@everywhere` to every module, function or variable you need to be used on multiple processor.

3. Define the range of parameters
4. Create a `dict_list`
5. Define the function that runs a single simulation, taking the dict of parameters and modifying one of the fields of the dict with the results (remember to preallocate the results!). The function should also save the results in a clean directory as a bson file.
6. `pmap(function, dict_list`, or `map(args)` if you're on a single processor
7. Later, to collect the results, you'll just need to run 

> using DataFrames
> df = collect_results!(datadir(*subdirectory*, *sub-subdirectory*))`

### Example with multiprocessing

```
@everywhere using DrWatson
@quickactivate "Ring Attractor"

@everywhere using Printf
using DataFrames

include(srcdir("utils.jl"))
include(srcdir("stats.jl"))
include_everywhere("../src/hebb.jl")

noise_range = [1, 2, 3]
fixed_points_range = [4, 8, 16]
seed = 42

d = dict_list(Dict("fixed_points"=>fixed_points_range,
				   "noise"=>noise_range,
				   "seed"=>seed,
				   "error"=>0.)


@everywhere function f(par)
	hring = HebbRing()
	hring(ϵ=par["noise"], fpn=par["fixed_points"], seed=par["seed"])

	par["error"] = sliding_filter(hring)[0]

	sname = savename((@dict par["noise"] par["fixed_points"), "bson")
	safesave(datadir("fixed_points", "random_simulation", sname), par)
end

pmap(f, d)

df = collect_results!(datadir("fixed_points", "random_simulation"))
```


