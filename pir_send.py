import os
import time 
import requests
from dotenv import load_dotenv
from gpiozero import MotionSensor

load_dotenv()
base = os.environ["API_BASE"]
key = os.environ["API_KEY"]
url = base + "/api/occupancy/DKIT_BUS_01/movement"
headers = {"X-API-Key": key}
data = {"direction": "in", "quantity": 1}
pir = MotionSensor(17)
print("Waiting for motion...")
while True:
    pir.wait_for_motion()
    r = requests.post(url, json=data, headers=headers)
    print("sent:", r.status_code)
    pir.wait_for_no_motion()
    time.sleep(2)
