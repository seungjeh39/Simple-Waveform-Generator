# Wave Generator - Seungjeh Lee

import RPi.GPIO as GPIO
import adafruit_mcp4725
import board
import busio
import math
from scipy import signal as sg
from time import sleep


GPIO.setmode(GPIO.BCM)

# Button
BUTTON_PIN = 5
GPIO.setup(BUTTON_PIN,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
sleep(1)
# Initialize MCP4725
dac = adafruit_mcp4725.MCP4725(i2c)

print("-- Setup Completed --")


# Triangle Wave function
def triangleWave(freq, maxVolt):
	t = 0.0
	tStep = 0.0007
	while True:
		voltage = (maxVolt/2) + (maxVolt/2)*sg.sawtooth(2*math.pi*freq*t, width=0.5)
		value = voltage * 4095 / 5.5
		if value > 4095:
			value = 4095
		if value < 0:
			value = 0
		dac.raw_value = int(value)
		t += tStep

		if (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
			break


# Square Wave Function
def squareWave(freq, maxVolt):
	t = 0.0
	tStep = 0.0008
	while True:
		voltage = (maxVolt/2) + (maxVolt/2)*sg.square(2*math.pi*freq*t)
		value = voltage * 4095 / 5.5
		if value > 4095:
			value = 4095
		if value < 0:
			value = 0
		dac.raw_value = int(value)
		t += tStep

		if (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
			break


# Sine Wave Function
def sineWave(freq, maxVolt):
	t = 0.0
	tStep = 0.0014
	while True:
		voltage = (maxVolt/2) + ((maxVolt/2)*math.sin(freq*2*math.pi*t))
		value = voltage * 4095 / 5.5
		if value > 4095:
		    value = 4095
		if value < 0:
		    value = 0
		dac.raw_value = int(value)
		t += tStep
		#sleep(0.0005)
		
		if (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
			break



try:
	while True:
		if (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
			print("1 = Triangle")
			print("2 = Square")
			print("3 = Sine")
			shape = int(input("Please select one of the numbers: "))
			freq = float(input("Please enter the frequency: "))
			maxVolt = float(input("Please enter the maximum output voltage: "))

			if shape == 1:
				triangleWave(freq, maxVolt)
			elif shape == 2:
				squareWave(freq, maxVolt)
			elif shape == 3:
				sineWave(freq, maxVolt)
			else:
				print("Invalid Input")

except KeyboardInterrupt:
	GPIO.cleanup()
