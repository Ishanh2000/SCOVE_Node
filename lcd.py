# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
from RPLCD.i2c import CharLCD
from sys import argv
from time import sleep

lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

def clearLCD():
	lcd.clear()

def writeLCD(s = ""):
	lcd.write_string(s)

def rewriteLCD(s = ""):
	lcd.clear()
	lcd.write_string(s)


if __name__ == "__main__":

	doLoop = (len(argv) > 1) and (argv[1] == "--loop")

	while True:
		rewriteLCD("HELLO WORLD!\r\nI AM AN LCD.")
		if not doLoop: break
		sleep(2)
		rewriteLCD("BYE WORLD!!")
		sleep(2)
