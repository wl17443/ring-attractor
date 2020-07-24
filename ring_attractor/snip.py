import numpy as np
import matplotlib.pyplot as plt

def G_ex(t): 
    return k_ex*t*np.exp(-t/T_syn_ex) 

T_syn_ex = 0.005                                                                    

k_ex = 1/(T_syn_ex*np.exp(-1))                                                      

times = np.linspace(0, 0.2, 1000)

points = []
for t in times:
    points.append(G_ex(t))

plt.plot(points)
plt.show()
