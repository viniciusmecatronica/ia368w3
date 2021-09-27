#
#   Copyright (C) 2014 Eleri Cardozo
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# function result = FeatureDetection(global_poses, L, Pose)
# 
# argumentos:
# global_poses: /perception/laser/n/global_poses
# L (landmarks) obtido a partir de Lx e Ly [mm]: 
# import numy as np
# L = np.array([Lx,Ly])
# Pose: pose com th em rad
# 
# Vesao Python implemantada pelo aluno Davi Francisco Caetano dos Santos
# RA 228971
#
# Para testar em linha de comando (restthru rodando):
"""
import restthru as rt
import numpy as np
import FeatureDetection as fd
import landmarks as lm
rt.http_init()
pose, ret = rt.http_get('http://127.0.0.1:4950/motion/pose')
gposes, ret = rt.http_get('http://127.0.0.1:4950/perception/laser/1/global_poses')
L = np.array([lm.Lx, lm.Ly])
f = fd.FeatureDetection(gposes, L, pose)
print(f)
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from SplitAndMerge import SplitAndMerge

# --------------------------------------

epsRange = 100

epsBearing = 4*np.pi/180

# ---------------------------------------

# Passo 1 - Split and Merge

def FeatureDetection(global_poses, L, Pose):
  PointsX, PointsY, NPoints = SplitAndMerge(global_poses)

  L_x = L[0].tolist()
  L_y = L[1].tolist()

  if (len(NPoints) < 3):   # unica reta ?
    print("Nenhuma feature detectada\n")
    return

  # Passo 2 - Calculo da MAXIMA VEROSSIMILHANCA

  Z_range = []
  Z_bearing = []
  # As features dos landmarks verdadeiros relativas a posicao atual:
  for x, y in zip(L_x, L_y):
    Z_range.append(np.sqrt((x - Pose['x'])**2 + (y -  Pose['y'])**2)) # [mm]
    Z_bearing.append(np.arctan2(y- Pose['y'] , x - Pose['x']) - Pose['th']) # [rad]

  # Landmarks detectados no momento atual pelo sensor (com erro)

  l_x = []
  l_y = []

  for x, y, n in zip(PointsX,PointsY,NPoints):
    if n > 2:    # despreza retas comapenas 2 pontos
      l_x.append(x)
      l_y.append(y)

  z_range = []
  z_bearing = []

  # Features atuais
  for x, y in zip(l_x,l_y):
    z_range.append(np.sqrt((x - Pose['x'])**2 + (y - Pose['y'])**2)) # [mm]
    z_bearing.append(np.arctan2(y - Pose['y'], x - Pose['x']) - Pose['th']) # [rad]

  detected_x = []
  detected_y = []
  real_x = []
  real_y = []
  deltaBearing_array = []

  for i in range(0,len(z_range)):
    for j in range(0,len(Z_range)):
        deltaRange = abs(z_range[i] - Z_range[j])
        deltaBearing = abs(z_bearing[i] - Z_bearing[j])
        if (deltaRange < epsRange and deltaBearing < epsBearing):
          detected_x.append(l_x[i])
          detected_y.append(l_y[i])
          real_x.append(L_x[j])
          real_y.append(L_y[j])
          deltaBearing_array.append(deltaBearing)

  plt.scatter(real_x , real_y,color='red')
  plt.scatter(detected_x,detected_y,color='green')
  plt.scatter(detected_x , detected_y,color='blue')
  plt.show()

  return detected_x, detected_y, real_x, real_y, deltaBearing_array
  
