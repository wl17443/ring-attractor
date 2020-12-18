using DrWatson
@quickactivate "Ring Attractor"

using DataFrames
using Plots
using Printf
using StatsPlots
using Statistics

include(srcdir("utils.jl"))

df = collect_results!(datadir("stability", "fixed-points-with-noise"))

plotlyjs()
@df df scatter(:e, :i, :count_inside, size=(800, 800), xlabel="Excitatory weights", ylabel="Inhibitory weights", label="Spikes inside", markersize=0.1, markerstrokecolor=:blue)
@df df scatter!(:e, :i, :count_outside, size=(800, 800), xlabel="Excitatory weights", ylabel="Inhibitory weights", label="Spikes outside", markersize=0.1, markerstrokecolor=:orange )
