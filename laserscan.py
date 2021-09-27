import sys
# sys.path.append('/usr/local/restthru/APIs/Python')
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import time
import restthru

host = 'http://127.0.0.1:4950'
# inicia API
restthru.http_init()
# obtem leituras do laser
laser = '/perception/laser/1/global_poses'
rposes,code = restthru.http_get(host+laser)
# Gira o robo
delta = 180
status,code = restthru.http_put(host+'/motion/heading', delta)
# verifica se o giro foi completado
progress = 1
while progress != 0:
	time.sleep(1)
	progress,code = restthru.http_get(host+'/motion/heading/status')
# obtem leituras do laser
rposes2,code = restthru.http_get(host+laser)
rposes += rposes2
# computa vertices da figura
vertices = []
codes = []
for i in range(len(rposes)):
	vertices += [(rposes[i]['x'], rposes[i]['y'])]
	codes += [Path.LINETO]
codes[0] = Path.MOVETO
codes[i] = Path.CLOSEPOLY
vertices = np.array(vertices, float)
path = Path(vertices, codes)
pathpatch = PathPatch(path, facecolor='None', edgecolor='blue')
# plota figura
fig, ax = plt.subplots()
ax.add_patch(pathpatch)
ax.set_title('Mapa do Ambiente')
ax.dataLim.update_from_data_xy(vertices)
ax.autoscale_view()
plt.show()


