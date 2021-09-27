# Baseado no código postado em:
# https://stackoverflow.com/questions/10952060/plot-ellipse-with-matplotlib-pyplot-python
# Adaptado por Eleri Cardozo, 2021

import numpy as np
# from matplotlib import pyplot as plt
from math import pi, cos, sin

def plotEllipse(x, y, a, b, theta, plt, steps=36):
    # x: x-position of the center
    # y: y-position of the center
    # a: radius on the x-axis
    # b: radius on the y-axis
    # theta: rotation angle
    # steps: number of points of the ellipse

    theta = -theta
    t = np.linspace(0, 2*pi, steps)
    Ell = np.array([a*np.cos(t) , b*np.sin(t)])  
    #u,v removed to keep the same center location
    R_rot = np.array([[cos(theta) , -sin(theta)],[sin(theta) , cos(theta)]])  
    #2-D rotation matrix
    Ell_rot = np.zeros((2,Ell.shape[1]))
    for i in range(Ell.shape[1]):
       Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])

    plt.plot( x+Ell_rot[0,:] , y+Ell_rot[1,:],'darkorange' )  #rotated ellipse
    plt.grid(color='lightgray',linestyle='--')
    return plt

if __name__ == "__main__":
    plotEllipse(3, 4, 5, 6, -30)
