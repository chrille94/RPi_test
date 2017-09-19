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
rMotor = GPIO.PWM(rMotorPWM, 100)  # Right motor PWM init @ 100Hz
lMotor = GPIO.PWM(lMotorPWM, 100)  # Left motor PWM init @ 100Hz

def getSensors():
    linereading = [GPIO.input(lSensor), GPIO.input(mSensor), GPIO.input(rSensor)]
    # print(linereading)
    return linereading

def decideSpeed():
    sensorval = getSensors()
    # print(sensorval)
    if(sensorval == [1, 1, 1]) or (sensorval == [0, 1, 0]):
        direction = (100, 100)
    elif(sensorval == [1, 1, 0]):
        direction = (40, 80)
    elif(sensorval == [0, 1, 1]):
        direction = (80, 40)
    elif(sensorval == [1, 0, 0]):
        direction = (0, 80)
    elif(sensorval == [0, 0, 1]):
        direction = (80, 0)
    elif(sensorval == [1, 0, 1]):
        direction = (0, 0)
    elif(sensorval == [0, 0, 0]):
        direction = (-50, -50)
    # print(direction)
    runMotor(direction)

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



while 1:
    decideSpeed()