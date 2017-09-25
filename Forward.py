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
rSensor = 18
mSensor = 23
lSensor = 24

GPIO.setmode(GPIO.BCM)

gpio_outputs = (rMotorPWM, rMotorF, rMotorR, lMotorPWM, lMotorF, lMotorR)

gpio_inputs = (rSensor, mSensor, lSensor)

GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(gpio_inputs, GPIO.IN)
rMotor = GPIO.PWM(rMotorPWM, 200)  # Right motor PWM init @ 100Hz
lMotor = GPIO.PWM(lMotorPWM, 200)  # Left motor PWM init @ 100Hz


def runMotor(values):
    if(values[0] == 0):
        lMotor.stop()
    else:
        lMotor.start(abs(values[0]))

    if(values[1] == 0):
        rMotor.stop()
    else:
        rMotor.start(abs(values[1]))
    # print(abs(values[0]))
    # print(abs(values[1]))

    if(values[0] >= 0):
        GPIO.output(lMotorR, 0)
        GPIO.output(lMotorF, 1)
    else:
        GPIO.output(lMotorF, 0)
        GPIO.output(lMotorR, 1)

    if(values[1] >= 0):
        GPIO.output(rMotorR, 0)
        GPIO.output(rMotorF, 1)
    else:
        GPIO.output(rMotorF, 0)
        GPIO.output(rMotorR, 1)

def cleanupGpio():
    GPIO.cleanup()

while 1:
    try:
        runMotor(100, 100)
    except KeyboardInterrupt:
        print "cleanup"
        cleanupGpio()
