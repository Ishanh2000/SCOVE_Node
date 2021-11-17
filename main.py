# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import cv2
import numpy as np
from time import time, sleep
from threading import Thread
import requests
from base64 import b64decode
import pickle

import face_tflite
import infer

from lcd import clearLCD, writeLCD, rewriteLCD
from mlx import getTemperature
from prox import isMotion
from gpiozero import Button

from comm import queueEvent, queueAttendance

IMG_PATH = "./img/"
TEMPERATURE_THRESHOLD = 30.0
SERVER_URI = "http://ec2-18-222-200-30.us-east-2.compute.amazonaws.com:5000"
b = Button(5)
LOG_PHASE_1 = True
LOG_PHASE_2 = True
LOG_PHASE_3 = True
LOG_ATT = True # do not change to false

def capture(imgPath):
  v = cv2.VideoCapture(0)
  _, img = v.read()
  cv2.imwrite(imgPath, img)

def getUpdateFlag():
  n = 5
  sum = 0
  for _ in range(n):
    sum += 1 if b.is_pressed else 0
    sleep(0.02) # 20 ms
  return (sum/n) >= 0.5


def main():
  print("#" * 50)

  while True:
    
    if getUpdateFlag():
      rewriteLCD("Please remove\r\nyour finger")
      while getUpdateFlag(): sleep(0.05)
      rewriteLCD("Updating...")

      req = requests.get(SERVER_URI + "/register")
      resp = req.json()
      f_faces = open("labels/face_labels.txt", "wb")
      f_svc = open("models/svc.pkl", "wb")
      f_faces.write(b64decode(resp["faces"]["content"]))
      f_svc.write(b64decode(resp["svc"]["content"]))
      f_faces.close()
      f_svc.close()

      # RECOMPUTE UPDATABLES
      face_tflite.face_classifier = pickle.loads(open('models/svc.pkl', "rb").read())
      infer.face_labels = infer.load_labels('labels/face_labels.txt')

      rewriteLCD("Updated!")
      sleep(1)


    if not isMotion():
      sleep(0.05)
      continue

    start = time()

    rewriteLCD("Welcome!")

    #### PHASE 1 (MAJOR EVENT) ####
    faceMaskStatus = None
    phase_1_img = []
    for i in range(3): # maximum three attempts (spacing = 0.5s) to detect face and mask
      img_name = f"{start}_p1_{len(phase_1_img)}.png"
      capture(IMG_PATH + img_name)
      faceMaskStatus = infer.detectFaceAndMask(IMG_PATH + img_name)
      phase_1_img.append({ "name" : img_name, "time" : time(), "status" : faceMaskStatus })
      if faceMaskStatus != None: break
      sleep(0.5)
    
    isMischief = (faceMaskStatus == None)

    if LOG_PHASE_1 : Thread(target = queueEvent, args=(start, 1, phase_1_img, isMischief)).start() # will delete images later

    if isMischief:
      rewriteLCD("Will report\r\nmischief!")
      sleep(2)
      continue

    if faceMaskStatus["maskLabel"] != "unmasked":
      rewriteLCD("Please remove\r\nyour mask!")
      sleep(1.5)

    rewriteLCD("Taking\r\nAttendance...")

    #### PHASE 2 (MAJOR EVENT) ####
    faceRecogStatus = None
    phase_2_img = []
    for i in range(3): # maximum 3 attempts to take opimistic attendance
      img_name = f"{start}_p2_{len(phase_2_img)}.png"
      capture(IMG_PATH + img_name)
      faceRecogStatus = infer.recognizeFace(IMG_PATH + img_name)
      phase_2_img.append({ "name" : img_name, "time" : time(), "status" : faceRecogStatus })
      if faceRecogStatus != None: break
      sleep(0.5)
    
    isMischief = (faceRecogStatus == None)

    if LOG_PHASE_2 : Thread(target = queueEvent, args=(start, 2, phase_2_img, isMischief)).start() # will delete images later

    if isMischief:
      rewriteLCD("Will report\r\nmischief!")
      sleep(2)
      continue

    rewriteLCD(faceRecogStatus["faceLabel"])
    sleep(0.5)

    rewriteLCD("Please wear mask")
    sleep(1.5)

    #### PHASE 3 (MAJOR EVENT) ####
    faceMaskTempStatus = None
    phase_3_img = []
    temps = [] # will take average later

    for i in range(3): # maximum 3 attempts to detect face/mask/temperature
      img_name = f"{start}_p3_{len(phase_3_img)}.png"
      capture(IMG_PATH + img_name)
      faceMaskTempStatus = infer.detectFaceAndMask(IMG_PATH + img_name)
      t = getTemperature()
      phase_3_img.append({ "name" : img_name, "time" : time(), "status" : faceMaskTempStatus, "temperature" : t })
      if faceMaskTempStatus != None:
        temps.append(t)
        if faceMaskTempStatus["maskLabel"] == "masked": break
      sleep(0.5)
    
    isMischief = (faceMaskTempStatus == None)

    if LOG_PHASE_3 : Thread(target = queueEvent, args=(start, 3, phase_3_img, isMischief)).start() # will delete images later

    if isMischief:
      rewriteLCD("Will report\r\nmischief!")
      sleep(2)
      continue

    avg_t = np.average(temps)
    
    disallowReason = ""
    if faceMaskTempStatus["maskLabel"] != "masked": disallowReason += "No/Improper mask\r\n"
    if avg_t > TEMPERATURE_THRESHOLD: disallowReason += "High temp.\r\n"

    if LOG_ATT : Thread(target = queueAttendance, args=(start, time(), faceRecogStatus["faceLabel"], avg_t, faceMaskTempStatus["maskLabel"], disallowReason)).start()

    if disallowReason == "": rewriteLCD("Please enter")
    else:
      rewriteLCD(disallowReason)
      sleep(1.5)
      rewriteLCD("Access Denied")

    sleep(1)
    clearLCD()


if __name__ == "__main__":
  main()
