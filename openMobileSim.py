import os
from restthru import *
import json

def openMobileSim():
	os.chdir('/usr/local/MobileSim/')
	os.system("/usr/local/MobileSim/MobileSim -m feec.map > /dev/null &")
	# os.system("service restthru start")
	os.system("service restthru stop")
	os.system("service restthru start")
	os.system("chromium http://localhost:4950/web/")

def startmoving(host='http://127.0.0.1:4950'):
	# tentei mas nao funcionou
	http_init()

	act1 = "/behaviour/avoidFront/"
	act2 = "/behaviour/avoidSide/"
	act3 = "/behaviour/bumpers/"
	act4 = "/behaviour/stallRecover/"
	act5 = "/behaviour/limiterForwards/"
	act6 = "/behaviour/limiterBackwards/"
	act7 = "/behaviour/constantVelocity/"
	act8 = "/behaviour/goTo/"

	pay1 = json.dumps({"obstacleDistance": "500", "avoidVelocity": "100" , "turnAmount": "15", "priority": "8"})
	pay2 = json.dumps({"obstacleDistance": "200" , "turnAmount": "5" , "priority": "8"})
	pay3 = json.dumps({"backOffSpeed": "100" , "backOffTime": "3000" , "turnTime": "3000" , "priority": "9"})
	pay4 = json.dumps({"obstacleDistance": "200" , "cyclesToMove": "50" , "speed": "100" , "degreesToTurn": "45" , "priority": "7"})
	pay5 = json.dumps({"stopDistance": "250" , "slowDistance": "1000" , "slowSpeed": "100" , "priority": "6"})
	pay6 = json.dumps({"stopDistance": "-250" , "slowDistance": "-500" , "maxBackwardsSpeed": "-100" , "priority": "6"})
	pay7 = json.dumps({"constantVelocity":"100" , "priority": "5"})
	pay8 = json.dumps({"pose": {"x": "200" , "y": "200" , "th": "200"}, "closeDist": "200" , "speed": "200" , "priority": "1"})

	retdata1, status1 = http_put(host+act1, pay1)
	retdata2, status2 = http_put(host+act2, pay2)
	retdata3, status3 = http_put(host+act3, pay3)
	retdata4, status4 = http_put(host+act4, pay4)
	retdata5, status5 = http_put(host+act5, pay5)
	retdata6, status6 = http_put(host+act6, pay6)
	retdata7, status7 = http_put(host+act7, pay7)
	retdata8, status8 = http_put(host+act8, pay8)




