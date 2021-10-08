# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
from smbus2 import SMBus
from mlx90614 import MLX90614
from time import sleep

t_sensor = MLX90614(SMBus(1), address=0x5A)

while (True):
  print(f"AMBIENT = {t_sensor.get_ambient()}")
  print(f"OBJECT1 = {t_sensor.get_object_1()}")
  print()
  sleep(1)
