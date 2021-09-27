import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
import time
from math import sqrt, sin, cos, pi
from openMobileSim import *
from restthru import *
from plotEllipse import plotEllipse
from normAngle import *

# openMobileSim()

# valores iniciais
# host = 'http://127.0.0.1:4950' #pelo LINUX
host = 'http://192.168.0.14:4950' #pelo WINDOWS
posit = '/motion/pose'
laser = '/perception/laser/1/distances?range=-90:90:5)'
heading = '/motion/heading'
vels = '/motion/vel2'

http_init()


K = 0.005

sigmaP = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype = np.float64)
R = np.array([[0.01, 0, 0], [0, 0.01, 0], [0, 0, .01]], dtype = np.float64) 
b = 165
betha_elipse = 0

# montar mapa
x1 = [0,4680,0,0,0,4680,4680,4680]
x2 = [0,920,920,920]
x3 = [4190,4680,4190,4190]
x4 = [4030,4680]
y1 = [0,0,0,3200,3200,3200,0,3200]
y2 = [2280,2280,2280,3200]
y3 = [2365,2365,2365,3200]
y4 = [0,650]
plt.plot([x for x in x1],[y for y in y1],'b')
plt.plot([x for x in x2],[y for y in y2],'b')
plt.plot([x for x in x3],[y for y in y3],'b')
plt.plot([x for x in x4],[y for y in y4],'b')
plt.axis('equal')

# model_X = 2340 
# model_Y = 1600
# model_Th = 0
pose,code=http_get(host+posit)
model_X = pose['x']
model_Y = pose['y']
model_Th = pose['th']*pi/180


now = time.time()

for iteration in range(120):
	print(iteration)

	# posicao
	pose,code=http_get(host+posit)
	odom_X = pose['x']
	odom_Y = pose['y']
	odom_Th = pose['th']*pi/180
	odom_Th = normAngle(odom_Th)


	vel,code=http_get(host+vels)
	velR = vel['right']
	velL = vel['left']

	# Plot e Print


	omgX = sigmaP[0][0] # omgX**2
	omgY = sigmaP[1][1] # omgY**2
	omgXY = sigmaP[1][0]
	a_elipse = sqrt(.5*(omgX+omgY+sqrt((omgY-omgX)**2+4*(omgXY**2))))
	b_elipse = sqrt(.5*(omgX+omgY-sqrt((omgY-omgX)**2+4*(omgXY**2))))	
	print("a",a_elipse,"b",b_elipse)
	if omgXY==0 and omgX<omgY: 
		betha_elipse = pi/2
	elif omgXY==0:
		betha_elipse = 0
	else:
		# betha_elipse = np.arctan2((a_elipse**2)-omgX,omgXY)
		betha_elipse = .5*np.arctan(2*omgXY/(omgY-omgX))+pi/2
		
	betha_elipse = normAngle(betha_elipse)

	print("betha_elipse",betha_elipse*(180/pi),"perp",betha_elipse*(180/pi)+90)
	print(sigmaP)

	# Calcula modelo cinematico

	delta_S = (velR+velL)/2
	delta_Th = (velR-velL)/(2*b)	
	Th_delta = model_Th + delta_Th/2	

	
	model_X = model_X + delta_S*cos(Th_delta)
	model_Y = model_Y + delta_S*sin(Th_delta)
	model_Th = model_Th + delta_Th
	model_Th = normAngle(model_Th)
	
	plt = plotEllipse(model_X,model_Y,a_elipse,b_elipse,betha_elipse,plt)	


	# Calcula G, V e Covariancia	
	G = np.array([[1, 0, -delta_S*sin(Th_delta)], [0, 1, delta_S*cos(Th_delta)], [0, 0, 1]], dtype = np.float64)
	# V = np.array([[.5*cos(Th_delta)-(delta_S/(4*b))*sin(Th_delta), .5*cos(Th_delta)+(delta_S/(4*b))*sin(Th_delta)],
	# 	[.5*sin(Th_delta)+(delta_S/(4*b))*cos(Th_delta), .5*sin(Th_delta)-(delta_S/(4*b))*cos(Th_delta)], 
	# 	[1/(2*b), -1/(2*b)]], dtype = np.float64)
	V = np.array([[cos(Th_delta), -.5*delta_S*sin(Th_delta)],[sin(Th_delta), .5*delta_S*cos(Th_delta)],[0, 1]], dtype = np.float64)

	# sigmaS = np.array([[K*abs(velR), 0], [0, K*abs(velL)]], dtype = np.float64)
	sigmaS = np.array([[K*abs(delta_S), 0], [0, K*abs(delta_Th)]], dtype = np.float64)

	sigmaP_linha = G.dot(sigmaP).dot(G.T) + V.dot(sigmaS).dot(V.T) + R
	
	sigmaP = sigmaP_linha

	print("odom \t",odom_X,"\t",odom_Y,"\t",odom_Th*(180/pi))
	print("model \t",model_X,"\t",model_Y,"\t",model_Th*(180/pi))
	print("vels \t",velR,"\t",velL)
	to = matplotlib.markers.MarkerStyle(marker='_')
	to._transform = to.get_transform().rotate(odom_Th)
	tm = matplotlib.markers.MarkerStyle(marker='_')
	tm._transform = tm.get_transform().rotate(model_Th)	
	plt.scatter(odom_X, odom_Y, marker=to,color='green', s=30)
	plt.scatter(model_X, model_Y, marker=tm,color='red', s=30)	

	delta_T = time.time()-now
	print("delta_T", delta_T)	
	if delta_T<1: time.sleep(1-delta_T)
	now = time.time()

plt.show()