from gpiozero import MotionSensor
from time import sleep 

pir = MotionSensor(17)
print("Waiting for motion...")
while True:
 pir.wait_for_motion()
 print("motion detected")
 pir.wait_for_no_motion()
 sleep(0.5)
