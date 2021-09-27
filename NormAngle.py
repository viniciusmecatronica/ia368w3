import math

def NormAngle(angle): # angle em radianos
   angle = angle % 2*math.pi
   if angle > math.pi:
      angle = angle - 2*math.pi
   elif angle < -math.pi:
      angle = angle + 2*math.pi
   return angle
