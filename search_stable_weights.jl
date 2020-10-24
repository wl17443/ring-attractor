using Plots
include("ring_attractor.jl")
include("stats.jl")


function fit_errors(N, fp, par)
    sim=SimulationParameters(64, 10000, 5e-4, fp, 0, 0.05, -0.10, 0.05, -0.25)
    means = zeros(N)
    vars = zeros(N)
    for i in 1:N
       m, v = sliding_filter(simulate(par,sim), sim)
       means[i] =  m
       vars[i] = v
    end
    fit(Gamma, means), fit(Gamma, vars) #TODO select distribution
end

# stable_mean, stable_var = fit_errors(1000, (24, 40), par)
# unstable_mean, unstable_var = fit_errors(1000, (), par)

function isstable(m, v, sm, sv, um, uv)
    loglikelihood(sm, m) + loglikelihood(sv, v) > loglikelihood(um, m) + loglikelihood(uv, v)
end

function find_stability_range(par)
    stable_exc, stable_inh, unstable_exc, unstable_inh, seeds = [],[],[],[],[]
    for exc in 0.05:0.01:0.1
        for inh in 0.05:0.01:0.25
            seed = rand(1:20000, 1)[1]

            sim=SimulationParameters(64, 10000, 5e-4, (24, 40), seed, .05, -.10, exc, -inh)

            m, v = sliding_filter(simulate(par, sim), sim) # We could get this from more trials
            if isstable(m, v, stable_mean, stable_var, unstable_mean, unstable_var)
                push!(stable_exc, sim.w_exc_fp)
                push!(stable_inh, sim.w_inh_fp)
            else
                push!(unstable_exc, sim.w_exc_fp)
                push!(unstable_inh, sim.w_inh_fp)
            end
            push!(seeds, seed)

        end
    end
    stable_exc, stable_inh, unstable_exc, unstable_inh, seeds
end

function find_stability_range(par, iters, exc_low, exc_high, inh_low, inh_high, step=0.01)
    stable_exc, stable_inh, unstable_exc, unstable_inh  = [],[],[],[]

    for exc in exc_low:step:exc_high
        for inh in inh_low:step:inh_high
            sim=SimulationParameters(64, 10000, 5e-4, (24, 40), 0, .05, -.10, exc, -inh)
            means, vars = [], []

            for _ in 1:iters
                m, v = sliding_filter(simulate(par, sim), sim) # We could get this from more trials
                push!(means, m)
                push!(vars, v)
            end

            if isstable(mean(means), mean(vars), stable_mean, stable_var, unstable_mean, unstable_var)
                push!(stable_exc, sim.w_exc_fp)
                push!(stable_inh, sim.w_inh_fp)
            else
                push!(unstable_exc, sim.w_exc_fp)
                push!(unstable_inh, sim.w_inh_fp)
            end

        end
    end
    stable_exc, stable_inh, unstable_exc, unstable_inh
end


function plot_stability_range(si, se, ui, ue)
    scatter(abs.(si), se, markershape = :rect, markersize = 5, lab="stable")
    scatter!(abs.(ui), ue, markershape = :rect, markersize = 5, lab="unstable")
    plot!(xaxis="Inhibitory weights")
    plot!(yaxis="Excitatory weights")

end

function check_idx(idx, stable_exc, stable_inh, unstable_exc, unstable_inh, seeds, stable=true)

    if stable
        exc = stable_exc[idx]
        inh = stable_inh[idx]
    else
        exc = unstable_exc[idx]
        inh = unstable_inh[idx]
    end
    sim=SimulationParameters(64, 1e5, 5e-4, (24, 40), seeds[idx], .05, -.10, exc, -inh)
    pot = simulate(par, sim)

    if stable
        tit = "Stable"
    else
        tit = "Unstable"
    end
    heatmap(pot, title=tit)
end
