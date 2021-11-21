# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
from smbus2 import SMBus # will cause problems if not using Raspberry Pi
from mlx90614 import MLX90614 # will cause problems if not using Raspberry Pi
from sys import argv
from time import sleep

t_sensor = MLX90614(SMBus(1), address=0x5A)

def getTemperature():
	return t_sensor.get_object_1()

if __name__ == "__main__":
	doLoop = (len(argv) > 1) and (argv[1] == "--loop")
	while (True):
		print(f"AMBIENT = {round(t_sensor.get_ambient() , 6)} \u00b0C")
		print(f"OBJECT1 = {round(t_sensor.get_object_1(), 6)} \u00b0C")
		print()
		if not doLoop: break
		sleep(1)
