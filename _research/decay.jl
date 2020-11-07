using Plots
include(srcdir("ring-attractor.jl"));

function mean_activity(N, par)
    sim =SimulationParameters(64, 10000, 5e-4, (), 0, 0.05, -0.10, 0.05, -0.25)
    mean_rate = zeros(sim.N, N)
    mean_spikes = zeros(sim.N, N)
    for i in 1:N
        pot = simulate(par, sim)
        spikes = Array{Int32, 2}(pot .== 0)
        mean_spikes[:, i] = sum(spikes, dims=2)
        mean_rate[:, i] = view(mean_spikes, :, i) ./ sim.time
    end

    mean(mean_spikes, dims=2), mean(mean_rate, dims=2)
end

mean_spikes, mean_rate = mean_activity(1000, par);
bar(mean_rate, lab="Firing rate")
title!("Spikes for millisecond")

findall(mean_rate .> 0.098)  # The real fixed point
findall(mean_rate .> 0.090)  # Under this values there are the others

x0 = 1/0.098
x1 = 1/0.090

tmax = 2000 # Time needed to go to the wmax
rate = 0.098

wmin = 0.05
wmax = 0.30

y1 = (wmax - wmin) / tmax * rate

b = (log(y1) + sqrt((-log(y1))^2 + 4x0*x1))/2x1
a = exp(b * x1)

t = [1:1:15;]
f(x) = a*exp(-x/b)
plot(f.(t[9:end]), line = (5), lab="decay")
hline!([y1], line = (5, :dash), lab="y1")


function decay()
    w0 = 0.05
    inc = 0.01
    tau = x0/(log(w0+inc) - log(y1)) * 45

    w = zeros(2000)
    w[1] = w0 + inc
    for t in 1:1999
        if t % 9 == 0
            w[t] += inc
        end

        w[t+1] =  w[t]  - w[t]/tau
    end

    plot(w)
end

decay()
