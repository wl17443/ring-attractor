include("ring-attractor.jl")
include("stats.jl")

using .RingAttractor

noises = 0:1e-3:3e-3
fprange = [0, [2^n for n in 0:3]...]
iters = 10

errors = []
for noise in noises
    for fpn in fprange
        r = Ring(noise=noise, fps=(fpn+2,))
        for i in 1:iters
            r()
            push!(errors, kl_divergence(fit(Normal, slice(r.S, 1:3000)),
            				 fit(Normal, slice(r.S, 7000:10000))))

        end
    end
end
