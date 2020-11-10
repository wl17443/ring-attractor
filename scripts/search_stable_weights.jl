using DrWatson
@quickactivate "Ring Attractor"

include(srcdir("stability.jl"))

e0 = 0.01
e1 = 0.20
i0 = 0.00
i1 = 0.049
step = 0.001
noise = 0.5e-3
iters = 1

r_e = e0:step:e1
r_i = i0:step:i1

# m = find_stable_w(r_e, r_i, noise)
# tmp = @dict e0 e1 i0 i1 step noise iters
# safesave(datadir("stability", savename(tmp, "csv")), m)
m = find_stable_fp_w(r_e, r_i, [32], iters)
noise *= 1e3 
tmp = @dict e0 e1 i0 i1 step noise iters
safesave(datadir("stability", savename("fp", tmp, "csv")), m)
