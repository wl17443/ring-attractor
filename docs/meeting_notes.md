### Meeting 1

- [x] von mises fit on first x seconds and last x seconds
- [x] take the k-l divergence (super careful) between the 2 and this will be new error metric
- [x] for every fp-N plot error x noise with mean plotted enveloped in std


### Meeting 2

- [x] double check if von mises is equal if i compress the first and last third with firing rates
- [x] next simulation, get also kl between unprocessed first and last bit
- [x] plot errors with interval confidence
- [x] make gif of the bump
- [x] analyze the bump with other methods (pca? smt on MNE?)
- [x] can you check the firing pattern of neurons in a fixed point between when they first enter the fixed point, and then after a while


### Meeting 3

- [ ] Try to understand if being in a fixed point reduces the energy level of the network
- [x] Write a summary of what you did to calculate the noise where every fp_n situation is stable


### Meeting 4 

- [x] Analytic kl 
- [x] Compute divergence in sliding window 
- [x] We can compute length of vector of different in std, difference in mean, error between the two time points (not gaussian)
- [ ] If bump drift too much terminate

### Meeting 5

- [x] Presentation and plots
- [x] characterize noise
- [x] the stability parameters, with surface plot

### Meeting 6


- [ ] summarized mehrdad meeting
- [ ] redo fp weight stability plot counting spikes only in the surrounding of the fixed point

**wed after 3pm (meeting at 6.30)**

### Meeting 7 

Learning rule:

- [x] Correct start and end points of learning
- [ ] Start guessing learning rule (hebbian style)
- [ ] find a baseline level of activity

1. Find out coincidence for synapses
2. Implement hebbs, making it work with different noise and make sure it's simmetric
3. Look for the bounds of stability
4. Fix picture of connectivity (all arrows but light grey, colored arrows
