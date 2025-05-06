import numpy as np 
import math
import matplotlib.pyplot as plt 

#variable usuel
g=9.81

#<=> ẍ +  3*v(x)+ g=0

#example de function
def f(t,v):
    return g-3*v

"""
 * @author Serrano Lucas
 * @fn def RK2(f)
 * @brief Résoud une fonction avec la méthode de RungeKitta d'ordre 2
 *
 * @param f la fonction à résoudre
 * @param h le pas  
 * @param T Le temps maximal
"""

def RK2(f,h=0.01,T=10):
    temps=[]
    vitesse=[]
    t=0
    v=0
    k_1=0
    k_2=0
    while t<=T:
        k_1=h*f(t,v)
        k_2=h*f(t+(1/2)*h,v+(1/2)*k_1)
        v=v+k_2
        t+=h

        temps.append(t)
        vitesse.append(v)
    return temps,vitesse



"""
 * @author Serrano Lucas
 * @fn def Euler(f)
 * @brief Résoud une fonction avec la méthode de Euler d'ordre 2
 *
 * @param f la fonction à résoudre
 * @param h le pas  
 * @param T Le temps maximal
"""

def Euler(f,h=0.01,T=10):
    t=0
    v=0
    vitesse=[]
    temps=[]
    while t<=T:
        k=f(t,v)
        v=v+h*k
        t+=h

        temps.append(t)
        vitesse.append(v)
    return temps,vitesse

"""
 * @author Gende-Pambou Kevin
 * @fn def _formule_runge_4
 * @brief Applique la formule de Runge-kutta d'ordre 4 pour le terme suivant le terme d'entrée
 * @param h correspond à l'écart de temps entre t et t+h
 * @param t correspond la t-ième seconde pour calculer la vitesse au rang t
 * @param v correspond à la vitesse au rang t-h
 * @param f correspond à la fonction à résoudre
"""

def _formule_runge_4(h, t, v, f) :
    k1=h*f(t, v)
    k2=h*f(t+0.5*h, v+0.5*k1)
    k3=h*f(t+0.5*h, v+0.5*k2)
    k4=h*f(t+h, v+k3)
    return (v+1/6*(k1+2*k2+2*k3+k4))

"""
 * @author Gende-Pambou Kevin
 * @fn def resolution_runge_4
 * @brief Résoud une équation différentielle avec la méthode de Runge-Kutta d'ordre 4
 * @param f correspond à la fonction à résoudre
 * @param h correspond à l'écart de temps entre t et t+h
 * @param T correspond à la fin de l'intervalle pour pouvoir tracer la courbe de la fonction
"""

def RK4(f,h=0.01,T=10) :
    t=0
    v=0
    abscisse=[]
    ordonnee=[]
    while (t<T) :
        v=_formule_runge_4(h, t, v, f)
        abscisse.append(t)
        ordonnee.append(v)
        t+=h
    return abscisse,ordonnee


#Exemple utilisation
temps,vitesse=RK2(f)
