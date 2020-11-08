using DrWatson
@quickactivate "Ring Attractor"

include(srcdir("stability.jl"))

e0 = 0.01
e1 = 0.30
i0 = 0.05
i1 = 0.30
step = 0.001
noise = 0.
iters = 7

r_e = e0:step:e1
r_i = i0:step:i1

m = find_stable_w(r_e, r_i, noise, iters)
tmp = @dict e0 e1 i0 i1 step noise iters
safesave(datadir("stability", savename(tmp, "csv")), m)
m = find_stable_fp_w(r_e, r_i, [32], iters)
tmp = @dict e0 e1 i0 i1 step noise iters
safesave(datadir("stability", savename("fp", tmp, "csv")), m)
