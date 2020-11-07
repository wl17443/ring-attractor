# The Objective
Spiking neural networks are highly non-linear, but in certain cases the dynamics can be predictable.

Here we are exploring the parameter space of the **noise** injected into the network, which is responsible for **variance** in the outcome, and of the number of **fixed points**, that produce bias.

Due to the connectivity matrix used in these simulations, the higher the noise is, the more probable is that the bump is dragged into a fixed point. In contrast, with less fixed points, the bump has to travel more distance to find the first one. 

Being dragged in the fixed point causes the error to raise if the bump is not likely to diverge a lot from his trajectory, but if there is a lot of noise, the fixed point stops the drift and keeps the error fixed.

These experiments are intended to discover how many fixed points are optimal for a given level of noise 

# The Challenges

- [x] Establishing a workflow
- [x] Selecting a sensible metric
- [x] Finding the right parameters
- [x] Setting up large-scale simulations
- [ ] Analyzing data to find optimal trade-off

## Establishing a workflow

1. Simulation
2. Analysis
3. Observations
4. Debugging
5. Fixes and Parameter Tuning
6. Repeat

## Selecting a sensible metric

- Absolute difference of the starting point and the mean spike position at the last interval of time *Doesn't consider circularity*
- Same thing but using circular mean *Too much dependent on distribution of last values*
- Coefficient of linear regression fitted one spike distribution with fixed intercept *Doesn't consider variance nor circularity*
- **Fitting the first and last segment to a Von Mises distribution and taking the Kullback–Leibler divergence between the two**

This were tested with different starting points for the fitting process, trying to fit the mean index of spikes for each time point, and trying to take the relative entropy of the bare data, but the best performing solution was to fit the data to a Von Mises fixing the location of the distribution on the standard deviation of the data.

This solution is able to detect:

- Noise
- Variance
- Circularity
- Still bump
- Exploding bump
- Splitting bump

And has the best ability to discern if the sections considered are 

- One freely moving with low noise and one inside a bump (where is more stable)
- Both in the bump
- One freely moving but in another position and the other still inside the bump (should be very similar to the first)

## Finding the right parameters

The most stable weights that still let the bump move with high levels of noise are:

- Excitatory synapses: .05 
- Inhibitory synapses: .10
- Excitatory synapses in fixed points: .05
- Inhibitory synapses in fixed points: .25
- The number of neurons was set to 256
- The fixed point comprised 3 neurons, with 5 excitatory and 7 inhibitory synapses for each side
- The fixed points ranged from 0 to 32, where to bump was dragged into the bump even at low levels of noise
- The noise was tested between 0.8 to 3.0e-3
- The simulation time was 10 seconds
- The repetitions with different random seeds for every couple of parameters was at least 30

Also, the first results showed a bias caused by moving the starting point, so we fixed that moving the fixed points between conditions instead.

X axis: Fixed points number  
Y axis: Amount of error  
The noise rises going right and down  
![X axis: Fixed points number  
Y axis: Amount of error
The noise rises going right and down](https://github.com/wl17443/ring-attractor/blob/master/analyses/pic1.png)

## Setting up large-scale simulations

This was done thanks to a computer in Manchester, that can be used to connect on the Spinnaker. It has 32 cores and the tasks where parallelized, still for some simulations the time required surpassed the 200 hours.

We improved the performance compiling the differential equations for updating the voltage of the neurons (if needed can be probably sped up treating the whole network as a DataFrame and updating every column at the same time)

The data for every simulation is stored in a csv with the random seed and parameters set, then for the analysis it was averaged in a single dataset for every batch of simulations.

## Analyzing data to find optimal trade-off

With the next results we expect to observe that with every fixed point number condition has a level of noise after of which shows stability.  
Maybe with conditional empty for different levels of noise given the number of fixed points we can show the optimal number of fixed point for level of noise in terms of information content.

This paragraph will be completed after that