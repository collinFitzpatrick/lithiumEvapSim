#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:20:12 2023

@author: mparsons
"""

import numpy as np
import matplotlib.pyplot as plt

def P_vapor(T):
    # T [K]
    # P [Pa]
    return 10**(12.4037 - 8283.1/T - 0.7081*np.log10(T))


def G_max(T):
    # T [K]
    # G [uc]
    
    R = 8.3145 # [J/mol-K]
    g = 10 # [m/s^2]
    pi = 3.141593
    M = 6.941 # [g/mol] 
    
    #uc = 1 # [kg/m^2/s]
    #uc = 360 # [g/cm^2/hour]
    #uc = 0.1 # convert to [g/cm^2/s]
    uc = 0.1 * (6.022e23 / 6.941) # [1/cm^2/s]
    
    return P_vapor(T) / (g * np.sqrt(2*pi*R*T/M)) * uc



T_all = np.linspace(200,1400,1000)
G_all = G_max(273.0 + T_all)
print(G_all)

A = 10 * 10 # [cm^2]
Gamma_t = 1e22 # Target Lithium Evaporation Flux [Li / s]
y_plot = Gamma_t / A / G_all # [fraction of lithium coverage]




plt.plot(T_all, y_plot)

T_100 = np.interp(1, y_plot[::-1], T_all[::-1])
plt.plot(T_100, 1, 'go')
plt.plot([T_all[0],T_100],[1,1], '--', color = 'g')
plt.plot([T_100,T_100],[1,y_plot[-1]], '--', color = 'g')

T_10 = np.interp(0.1, y_plot[::-1], T_all[::-1])
plt.plot(T_10, 0.1, 'yo')
plt.plot([T_all[0],T_10],[0.1,0.1], '--', color = 'y')
plt.plot([T_10,T_10],[0.1,y_plot[-1]], '--', color = 'y')

T_1 = np.interp(0.01, y_plot[::-1], T_all[::-1])
plt.plot(T_1, 0.01, 'ro')
plt.plot([T_all[0],T_1],[0.01,0.01], '--', color = 'r')
plt.plot([T_1,T_1],[0.01,y_plot[-1]], '--', color = 'r')




plt.title('Fraction of %g cm^2 Area Covered in Lithium for Flux %g'%(A, Gamma_t))
plt.yscale("log")
plt.grid("on")
plt.xlabel("T / [C]")
plt.xlim([T_all[0],T_all[-1]])
plt.ylim([y_plot[-1],y_plot[0]])
plt.ylim(top=1.1)
plt.show()


"""
d = 0.1 # Hole diameter [cm]
y_plot = np.sqrt(Gamma_t / A / G_all / (np.pi * (d/2)**2))
N_max = 1/np.sqrt(np.pi * (d/2)**2)
T_min = np.interp(N_max, y_plot[::-1], T_all[::-1])

plt.plot(T_all, y_plot)
plt.plot([T_all[0], T_min], [N_max, N_max], '--', color = 'r')
plt.yscale("log")
plt.grid("on")
plt.xlabel("T / [C]")
plt.xlim([T_all[0],T_all[-1]])
plt.ylim([y_plot[-1],y_plot[0]])
plt.show()
"""
