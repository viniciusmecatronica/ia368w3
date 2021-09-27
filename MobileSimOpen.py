import os
from restthru import *

os.chdir('/usr/local/MobileSim/')
os.system("/usr/local/MobileSim/MobileSim -m feec.map > /dev/null &")
# os.system("service restthru start")
os.system("service restthru stop")
os.system("service restthru start")
os.system("chromium http://localhost:4950/web/robot_action.html")


