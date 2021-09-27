import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
import time
import math

# mapa
tamCel = 50
numCelX = 200
numCelY = 200
mapa = np.zeros([numCelX,numCelY])

# pose do robo
px = 3000
py = 1500
pth = 15*np.pi/180  # rad

# leitura do laser
r = 2000
fi = 20*math.pi/180

# dados do laser
precisao = 50 
passo = 1*np.pi/180  # rad
mu = np.array([r, fi],  dtype = np.float)

sigma = np.array([[2.0, 0], [0, 0.2]], dtype = np.float)
invSigma = np.linalg.inv(sigma)

Pmin = 0.4

K = 0.5

x = np.linspace(0, numCelX, numCelX)
y = np.linspace(0, numCelY, numCelY)
xx, yy = np.meshgrid(x, y)
max = 0

z = np.zeros([len(x),len(y)])

for i in range(0,len(x)):
    # posicao da celula (i, j) no referencial global
    xi = i*tamCel + tamCel/2
    for j in range(0,len(y)):
        yj = j*tamCel + tamCel/2
        # raio em relacao ao robo
        r = math.sqrt((xi - px)**2 + (yj - py)**2)
        # angulo em relacao ao robo
        b = np.arctan2((yj - py), (xi - px)) - pth
        gama = np.array([r, b],  dtype = np.float)
        # diferenca em relacao a leitura do sensor
        delta = gama - mu
        if abs(delta[1]) > 2*passo:
            continue
        if r < mu[0]:
            P = Pmin
        else:
            P = 0.5
        delta[0] = delta[0]/1000  # distancia em metros
        z[j,i] = P + (K/(2*np.pi*sigma[0,0]*sigma[1,1]) + 0.5 - P)*np.exp(-0.5*(np.dot(np.dot(delta,invSigma),delta.T)))
        mapa[j,i] = mapa[j,i] + np.log(z[j,i]/(1-z[j,i]))
        if z[j,i] > max:
           max = z[j,i]

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(xx, yy, mapa)
plt.show()
print("z máximo", max)
