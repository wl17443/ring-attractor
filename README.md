# Ring Attractor Network 
## Introduction
This repository holds the Neuromatch Academy 2020 project work of Stefano, Nikitas, Pranjal and Angela for a ring attractor network under the guidance of our pod TA, Peter Vincent and mentorship of Mehrdad Jazayeri.
## Scientific Question  
How to construct a biologically plausible, dynamic ring attractor network of firing neurons?
## Background 
The  ring attractor with bump like neural activity has been hypothesised to work as a biologically plausible model for memory. It can be used to model the dynamics of head direction, encoded by E-PG neurons of Ellipsoid Body of Drosophilla melanogoster and other cyclic parameters like colours.
## Methods 
Modelling of LIF neurons with a connectivity matrix of 4-4 topology  to construct a desirable  ring attractor. Subsequently, fix points are added  to the network along with normal white noise to make it more biologically plausible. Several iterations of simulation were run with altering parameters to find optimal parameters that allow the network to sustain its activity and behave in an explainable way. 
## Conclusions 
In conclusion, it was found that for a working model of a ring attractor, fixed points at various positions in the ring network are needed to prevent drifting caused by noise. The dynamics of the network are determined by a variety of parameters such as the balance between inhibitory and excitatory neurons, number of fixed points and the strength of the noise.
## Code
Please reference the Github Wiki of this repository for more information on the dirty details of our code.  

## What we have done
- [x] Built an IAF model with conductance based synapses
- [x] Connected 128 neurons with 2-4 connectivity rule in a ring
- [x] Found out the parameters to have a stable bump after an input
- [x] Implemented gaussian noise to every voltage update of every neuron
- [x] Manipulated simulation parameters so that bumps don't get ignited by noise 
- [x] Implemented fixed points as groups of 3 adjacent neurons with stronger excitatory and inhibitory weights
- [x] Implemented an equation to uodate weights as a function of number of fixed ponts
- [x] Implemented an error metric based on the mean of the median neuron that fired in every timestep for the last 100 timesteps
- [x] Performed many simulations with different fixed points to find the one with least error

## Yet to do

- [ ] Repeat simulations with different levels of noise
- [ ] Implement learning rules

## Resources
*Theoretical Neuroscience*, Peter Dayan and L. F. Abbot  
*Critical Limits in a Bump Attractor Network of Spiking Neurons*, Alberto Arturo Vergani and Christian Robert Huyck
