using DrWatson
@quickactivate "Ring Attractor"

include(srcdir("stability.jl"))

e0 = 0.00
e1 = 0.20
i0 = 0.00
i1 = 0.2
step = 0.001
seed=2020

r_e = e0:step:e1
r_i = i0:step:i1

m = find_stable_fp_w(r_e, r_i, [32], seed, true)
tmp = @dict e0 e1 i0 i1 step seed
safesave(datadir("stability", "fixed_points", "sum", savename("fp", tmp, "csv")), m)
