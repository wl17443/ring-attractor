from ScalingTools import *

neuronType = {
    "i": -80*mV,
    "e": 0*mV
}

neuronParams = {
    "El": -70*mV,
    "Tm": 20*ms,
    "RmIe": 18*mV,
    "thresholdPotential": -54*mV,
    "resetPotential": -80*mV,
    # synaptic parameters
    "Rmgs": 0.15,
    "maxs": 0.5,
    "Ts": 10*ms
}