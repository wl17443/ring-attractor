using DrWatson
@quickactivate "Ring Attractor"

using Plots
using Statistics
using StatsPlots
include(srcdir("ring-attractor.jl"))
include(srcdir("stats.jl"))


function fit_errors(fps, iters=500)
    ring = Ring(fps=fps)
    means = zeros(iters)
    vars = zeros(iters)

    @inbounds for i in 1:iters
        m, v = sim_and_measure(ring)
        @inbounds means[i] =  m
        @inbounds vars[i] = v
    end
    fit(Gamma, means[.!isnan.(means)]), fit(Gamma, vars[.!isnan.(vars)]) # TODO select distribution
end


function isstable(m, v, pars)
    sm, sv, um, uv = pars
    loglikelihood(sm, m) + loglikelihood(sv, v) > loglikelihood(um, m) + loglikelihood(uv, v)
end

function stability(m, v, pars)
    sm, sv, um, uv = pars
    loglikelihood(um, m) / loglikelihood(sm, m) + loglikelihood(uv, v) / loglikelihood(sv, v) 
end



function find_stability_range(pars, e_range=0.05:0.01:0.25, i_range=0.05:0.01:0.25, fps=[24, 38], iters=3)
    stability_matrix = zeros(length(e_range), length(i_range))

    @inbounds for (k, i) in enumerate(i_range)
        @inbounds for (j, e) in enumerate(e_range)
            ring = Ring(wₑᶠ=e, wᵢᶠ=i, fps=fps)

            @inbounds measures = [sim_and_measure(ring) for _ in 1:iters]
            @inbounds means = [i[1] for i in measures]
            @inbounds vars = [i[2] for i in measures]

            @inbounds stability_matrix[j, k] = isstable(means[.!isnan.(means)], vars[.!isnan.(vars)], pars)

        end
    end
    stability_matrix
end


function plot_stability_range(stability_matrix, r_e, r_i)
    heatmap(r_i, r_e, stability_matrix, c=:roma)
    yaxis!("Excitatory weights")
    xaxis!("Inhibitory weights")
end

function plot_curves(pars)
    plot([pars[[1,3]]..., pars[[2,4]]...], lw=3, layout=2, labels=["stable means" "stable variances" "unstable means" "unstable variances"])
    title!("Distributions of measures")
end    

r_e = 0.05:0.01:0.10
r_i = 0.05:0.01:0.20
fps = [32]
pars = [fit_errors(fps)..., fit_errors([])...]
plot_curves(pars)
sm = find_stability_range(pars, r_e, r_i, fps, 7)
plot_stability_range(sm, r_e, r_i)