# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import os
import json
import requests
from time import sleep, time
from threading import Thread

SERVER_URI = "http://127.0.0.1:5000"
IMG_PATH = "./img/"

def queueEvent(start, phase, imgBag, isMischief):
  files = { _img["name"] : open(IMG_PATH + _img["name"], "rb") for _img in imgBag }
  files['json'] = json.dumps({ "start" : start, "phase" : phase, "isMischief" : isMischief, "images" : imgBag })
  req = requests.post(SERVER_URI + "/events", files=files)
  print("EVENT:", req.content.decode("UTF-8"))
  for _img in imgBag: os.remove(IMG_PATH + _img["name"]) # UNCOMMENT THIS

def queueAttendance(start, attTime, faceLabel, avgTemp, maskLabel, disallowReason):
  jsonData = { "start" : start, "attTime" : attTime, "faceLabel" : faceLabel, "avgTemp" : avgTemp, "maskLabel" : maskLabel, "disallowReason" : disallowReason }
  req = requests.post(SERVER_URI + "/attendance", json=jsonData)
  print("ATTENDANCE:", req.content.decode("UTF-8"))

if __name__ == "__main__":
  start = 1636945318.324496
  phase = 3
  phase_3_img = [
    { "name" : f"{start}_p3_0.png", "time" : time()+0, "status" : None, "temperature" : 20.0 },
    { "name" : f"{start}_p3_1.png", "time" : time()+1, "status" : { "maskLabel" : "unmasked", "probability" : 0.956 }, "temperature" : 20.0 },
    { "name" : f"{start}_p3_2.png", "time" : time()+2, "status" : { "maskLabel" :   "masked", "probability" : 0.998 }, "temperature" : 30.0 },
  ]
  isMischief = False
  
  Thread(target = queueEvent, args=(start, phase, phase_3_img, isMischief)).start()

  Thread(target = queueAttendance, args=(start, time(), "unknown", 27.0, "masked", "some reason")).start()

  sleep(5)


    

