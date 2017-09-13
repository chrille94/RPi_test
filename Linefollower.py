#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time

# GPIO pin defs
rMotorPWM = 4
rMotorF = 3
rMotorR = 2
lMotorPWM = 17
lMotorF = 27
lMotorR = 22
sensor = 18

GPIO.setmode(GPIO.BCM)

gpio_outputs = (rMotorPWM, rMotorF, rMotorR, lMotorPWM, lMotorF, lMotorR)

# GPIO.setup(rMotorPWM, GPIO.OUT)
# GPIO.setup(rMotorF, GPIO.OUT)
# GPIO.setup(rMotorR, GPIO.OUT)
# GPIO.setup(lMotorPWM, GPIO.OUT)
# GPIO.setup(lMotorF, GPIO.OUT)
# GPIO.setup(lMotorR, GPIO.OUT)
GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)
rMotor = GPIO.PWM(rMotorPWM, 100)
lMotor = GPIO.PWM(lMotorPWM, 100)

while 1:
    if(GPIO.input(sensor) == True):
        lMotor.stop()
        GPIO.output(lMotorF, 0)
        rMotor.start(100)
        GPIO.output(rMotorF, 1)
    else:
        rMotor.stop()
        GPIO.output(rMotorF, 0)
        lMotor.start(100)
        GPIO.output(lMotorF, 1)
