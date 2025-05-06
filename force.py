import pygame as py
import random as rd
import numpy as np
import sys
import matplotlib.pyplot as plt 
from solve import *

"""
v^0=1.34 ms^-1
sqrt{\theta}=0.26 ms^-1
v_\alpha^max = 1.3 v_\alpha ^0

position aléatoire

R=0.2m


a= \frac{v_i^0(t) e_i^0(t) - v_i(t) }{t_i}
dv/dt =  \frac{v_i^0(t) e_i^0(t) - v_i(t) }{t_i}

"""
N=10
v_moyenne=1.34
ecart_type=0.26
tau=1

vitesse=np.random.normal(v_moyenne,ecart_type,N)

print(vitesse)
def f(t,v):
    return (vitesse[i] - v)/tau



plt.title(f"Vitesses des {N} piétons")

plt.ylabel("vitesse")
plt.xlabel("temps")
for i in range(0,N):

    t,v=RK4(f)
    plt.plot(t,v,label=f"Pieton {i}")
    plt.legend()
plt.show()