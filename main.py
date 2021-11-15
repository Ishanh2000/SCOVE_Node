# AUM SHREEGANESHAAYA NAMAH||
import cv2
import numpy as np
from time import time, sleep
from infer import detectFaceAndMask, recognizeFace

from lcd import clearLCD, writeLCD, rewriteLCD
from mlx import getTemperature
from prox import isMotion

IMG_PATH = "./img/"
TEMPERATURE_THRESHOLD = 30.0


def capture(imgPath):
  v = cv2.VideoCapture(0)
  _, img = v.read()
  cv2.imwrite(imgPath, img)


def main():
  print("#" * 50)

  while True:
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
      faceMaskStatus = detectFaceAndMask(IMG_PATH + img_name)
      phase_1_img.append({ "name" : img_name, "time" : time(), "status" : faceMaskStatus })
      if faceMaskStatus != None: break
      sleep(0.5)
    
    isMischief = (faceMaskStatus == None)

    # queueEvent(start, phase=1, phase_1_img, isMischief) # will delete images later

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
      faceRecogStatus = recognizeFace(IMG_PATH + img_name)
      phase_2_img.append({ "name" : img_name, "time" : time(), "status" : faceRecogStatus })
      if faceRecogStatus != None: break
      sleep(0.5)
    
    isMischief = (faceRecogStatus == None)

    # queueEvent(start, phase=2, phase_2_img, isMischief) # will delete images later

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
      faceMaskTempStatus = detectFaceAndMask(IMG_PATH + img_name)
      t = getTemperature()
      phase_3_img.append({ "name" : img_name, "time" : time(), "status" : faceMaskTempStatus, "temperature" : t })
      if faceMaskTempStatus != None:
        temps.append(t)
        if faceMaskTempStatus["maskLabel"] == "masked": break
      sleep(0.5)
    
    isMischief = (faceMaskTempStatus == None)

    # queueEvent(start, phase=3, phase_3_img, isMischief) # will delete images later

    if isMischief:
      rewriteLCD("Will report\r\nmischief!")
      sleep(2)
      continue

    avg_t = np.average(temps)
    
    disallowReason = ""
    if faceMaskTempStatus["maskLabel"] != "masked": disallowReason += "No/Improper mask\r\n"
    if avg_t > TEMPERATURE_THRESHOLD: disallowReason += "High temp.\r\n"

    # queueAttendance(start, time(), faceRecogStatus["faceLabel"], avg_t, faceMaskTempStatus["maskLabel"], disallowReason)

    if disallowReason == "": rewriteLCD("Please enter")
    else:
      rewriteLCD(disallowReason)
      sleep(1.5)
      rewriteLCD("Access Denied")

    sleep(1)
    clearLCD()
    

    



if __name__ == "__main__":
  main()
