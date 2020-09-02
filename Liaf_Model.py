from Scaling_Tools import *
import numpy as np 

class LIAF_Model:
    I_in = 0*nA # Input current 
    I_ect = 0*nA # Simulated ectopic current 
    C_m = 0.002*mu_F # Membrane capacitance  
    V_0 = -52*mV # Resting potential 
    R_m = 10*MOhm # Membrane resistance 
    V_thr = -45*mV # Firing threshold 
    V_max = 20*mV
    V_min = -72*mV

    t_AP = 2*ms # Length of an action potential 
    alpha, beta, gamma, delta = 0, 1, 0, 1 # Normalisation parameters so that the max and min of the Normpdf and sin segments are 1 and 0 respectively 

    I_PSC = 5*nA # Amplitude of a postsynaptic current 
    alpha_p, beta_p, gamma_p, delta_p = 0, 1, 0, 1 # Again, normalisation parameters
    t_PSC = 5*ms # Half life of PSC decay 

    def __init__(self, connections):
        self.V_i = self.V_0 
        self.PSA = 0*nA 
        self.connections = connections 
        self.post_spike_time = 0*ms 

    def step(self, psc):
        if self.V_i < self.V_thr: 
            self.V_i = self.V_i + self.v(psc)*dt 
            return self.V_i
        else:
            self.post_spike_time += dt

            return self.v_ps()
    
    # TODO This should be a template voltage trace that every time a neuron fires, it follows this voltage trace!
    def v_ps(self):
        if self.post_spike_time > 0 and self.post_spike_time < self.t_AP/2:
            return self.V_thr+((self.V_max-self.V_thr)*self.normpdf(0,1,-1+self.post_spike_time/self.t_AP/2)-self.alpha)/self.beta 
        elif self.post_spike_time > self.t_AP/2 and self.post_spike_time < self.t_AP:
            return self.V_min+(self.V_max-self.V_min)*(np.sin((self.post_spike_time-self.t_AP/2)*2*np.pi/self.t_AP+np.pi/2)+self.gamma)/self.delta

    def v(self, postsynaptic_input_current):
        return ((self.V_0-self.V_i)/self.R_m+self.I_in+np.multiply(self.connections, postsynaptic_input_current).sum()+self.I_ect)/self.C_m 

    def normpdf(self, mu, sigma, at):
        return 0 