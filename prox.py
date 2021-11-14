# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

def isMotion():
	return GPIO.input(11)

if __name__ == "__main__":
	while True:
		print(f"{GPIO.input(11)} ({time.time()})")
		time.sleep(0.2)

