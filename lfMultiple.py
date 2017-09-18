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
    print(linereading)
    return linereading


def forward():
    GPIO.output(rMotorR, 0)
    GPIO.output(lMotorR, 0)
    GPIO.output(rMotorF, 1)
    GPIO.output(lMotorF, 1)
    rMotor.start(100)
    lMotor.start(100)

def softRight():
    GPIO.output(rMotorR, 0)
    GPIO.output(lMotorR, 0)
    GPIO.output(rMotorF, 1)
    GPIO.output(lMotorF, 1)
    rMotor.start(60)
    lMotor.start(100)


def softLeft():
    GPIO.output(rMotorR, 0)
    GPIO.output(lMotorR, 0)
    GPIO.output(rMotorF, 1)
    GPIO.output(lMotorF, 1)
    rMotor.start(100)
    lMotor.start(60)


def hardRight():
    GPIO.output(rMotorF, 0)
    GPIO.output(lMotorR, 0)
    GPIO.output(rMotorR, 1)
    GPIO.output(lMotorF, 1)
    rMotor.start(100)
    lMotor.start(100)


def hardLeft():
    GPIO.output(rMotorR, 0)
    GPIO.output(lMotorF, 0)
    GPIO.output(rMotorF, 1)
    GPIO.output(lMotorR, 1)
    rMotor.start(100)
    lMotor.start(100)


def stop():
    rMotor.stop()
    lMotor.stop()


# options = {[0, 0, 0]: forward,  # All sensors see white
#            [1, 1, 1]: forward,  # All sensors see black
#            [0, 1, 0]: forward,  # Middle sensor black. Others: white
#            [0, 1, 1]: softRight,  # Left sensor: white. Others: black
#            [1, 1, 0]: softLeft,  # Right sensor: white. Others: black
#            [0, 0, 1]: hardRight,  # Right sensor: black. Others: white
#            [1, 0, 0]: hardLeft,  # Left sensor: black. Others: white
#            [1, 0, 1]: stop,  # Middle sensor white. Others: black
#            }


while 1:
    getSensors()
    time.leep(1)
    # options[linereading]()
    # if (linereading == [0, 0, 0] or [1, 1, 1] or [0, 1, 0]):
    #     forward()
    # elif (linereading == [0, 1, 1]):        # Left sensor: white. Others: black
    #     softRight()
    # elif (linereading == [1, 1, 0]):        # Right sensor: white. Others: black
    #     softLeft()
    # elif (linereading == [0, 0, 1])         # Right sensor: black. Others: white
    #     hardRight()
    # elif (linereading == [1, 0, 0]):        # Left sensor: black. Others: white
    #     hardLeft()
    # elif (linereading == [1, 0, 1]):        # Middle sensor white. Others: black
    #     stop()
