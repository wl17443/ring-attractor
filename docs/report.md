First, we explored the literature to find examples, and implemented a realistic drosophila-based model, but that didn't wasn't flexible enough for our exploration, so we followed the paper from [Vergani and Huyck](https://arxiv.org/abs/2003.13365).
To do that, we built an Integrate and fire neuron model, with conductance based synapses and exponential currents from scratch with Python, using a timestep constant of 1ms and implementing the Euler method to approximate the differential equations.   
We then connected the neurons with a 2-4 connectivity rule (2 excitatory synapses and then 4 inhibitory by each side) to form a ring.  
<!-- (I'm still working on a decent representation, that's what I've got so far) -->
<!-- ![connectiviy](connectivity.png) -->

After that, we injected noise into the network, trying with different sources (correlated noise, Ornstein-Uhlenbeck process, white noise) and we concluded that white noise was the most relevant for our study. The noise has mean 0 and standard deviation between 0 and 3e-3, and is computed indipendently for every neuron at every time step. We manually explored the behaviour of the network under different amount of noises, to find stable weight strenghts. To address self-ignition of bumps due to noise, we increased the membrane time constant by 1ms, without compromising the plausibility of the model. We also changed to connectivity from 2-4 to 5-7, to increase stability.

Then we started investigating the role of fixed points on reducing the variability of the bump position. We manually found the parameters to have a stable fixed point, and made multiple large-scale simulations, varying the number of fixed points and the amount of noise injected.

Fixed points are defined as groups of 3 neighbors neurons with different local weights, able to capture the bump and keep it in that position even in the presence of high noise.

The bump was always started in the middle of two fixed points, that was equispaced. That made it so that for example, with 100 neurons and 4 fixed points, the starting point would be farther away from the closer fixed point than in the case of 100 neurons and 12 fixed points.

The simulations drove us toward fixing some setup mistakes and exploring different error measures (mean, circular mean, centroid, fitted linear regression parameters) until developing a method able to capture:

- absence of activation
- explosion of activation
- small differences in variability of the bump shape
- small differences in the neurons activate at the beginning vs the end

The achieve that, Peter suggested to fit the first and the last third of the time course of the bump to a Von-Mises distribution, than to take the Kullback-Leibler divergence between the two distributions.

This process has slowed down the research, since simulations took around 1 week to run, so I decided to move the code on Julia.
The algorithm was parallelized, and the allocations needed to simulate it carefully managed, reducing the time to simulate 10 seconds of activity of 256 neurons from ~80 seconds with Python and Numba to ~0.3 seconds with plain Julia.

This allowed us to simulate the activity of the network with high sensibility and speed over different values of global excitatory and inhibitory weights, observing a bifurcation between stability and explosion over the diagonal of the weights matrix, so that every time the excitatory weights are greater than the inhibitory, the activity of the whole network becomes active.
Adding noise in the same simulation setup revealed that the bifurcation line moved so that excitatory weights need to be quite smaller than inhibitory to have stability.

We also repeated a similar simulation, but only changing local weights around the ignition point, and measuring activity only in that range. That allowed us to study for how weights needs to be changed localy to obtain a stable fixed point, so that we can use this knowledge as starting point to infer plasticity parameters that allow the autonomous formation of fixed point on neurons that has been stimulated.
