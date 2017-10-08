#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import threading

rMotorPWM = 4
rMotorF = 3
rMotorR = 2
lMotorPWM = 17
lMotorF = 27
lMotorR = 22
rSensor = 18
mSensor = 23
lSensor = 24
button1 = 16
button2 = 20
button3 = 21
sign1 = 19
sign5 = 26

GPIO.setmode(GPIO.BCM)

gpio_outputs = (rMotorPWM, rMotorF, rMotorR, lMotorPWM, lMotorF, lMotorR, sign1, sign5)

gpio_inputs = (rSensor, mSensor, lSensor, button1, button2, button3)

GPIO.setup(gpio_outputs, GPIO.OUT)
GPIO.setup(gpio_inputs, GPIO.IN)
rMotor = GPIO.PWM(rMotorPWM, 200)  # Right motor PWM init @ 200Hz
lMotor = GPIO.PWM(lMotorPWM, 200)  # Left motor PWM init @ 200Hz
oneSign = GPIO.PWM(sign1, 400)
fiveSign = GPIO.PWM(sign5, 400)

class saveDirection:
    lastDir = 0  # "static" variable accessed through class


class savePress:
    prev_input1 = 0
    prev_input2 = 0


class startFlag:
    started = 0


class blinkSign(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        oneSign.start(0)
        fiveSign.start(0)
        while 1:
            for i in range(20, 100, 1):
                oneSign.ChangeDutyCycle(i)
                fiveSign.ChangeDutyCycle(i)
                time.sleep(0.01)

            for j in range(100, 20, -1):
                oneSign.ChangeDutyCycle(j)
                fiveSign.ChangeDutyCycle(j)
                time.sleep(0.01)


def readButtons():
    startButton = GPIO.input(button1)
    stopButton = GPIO.input(button3)
    if ((savePress.prev_input1) and not startButton):
        print("start pressed")
        startFlag.started = 1
    if ((savePress.prev_input2) and not stopButton):
        print("Stop pressed")
        startFlag.started = 0

    savePress.prev_input1 = startButton
    savePress.prev_input2 = stopButton


def getSensors():
    leftReadings = [0] * 15
    middleReadings = [0] * 15
    rightReadings = [0] * 15
    linereading = [0] * 3
    for i in range(0, 15):
        leftReadings[i] = GPIO.input(lSensor)
        middleReadings[i] = GPIO.input(mSensor)
        rightReadings[i] = GPIO.input(rSensor)
    if (leftReadings.count(1) > 3):
        linereading[0] = 1
    else:
        linereading[0] = 0

    if (middleReadings.count(1) > 3):
        linereading[1] = 1
    else:
        linereading[1] = 0

    if (rightReadings.count(1) > 3):
        linereading[2] = 1
    else:
        linereading[2] = 0

    return linereading


def decideSpeed():
    sensorval = getSensors()
    # print(sensorval)
    if (sensorval == [1, 1, 1]) or (sensorval == [0, 1, 0]):
        direction = (100, 100)
    elif (sensorval == [1, 1, 0]):
        direction = (50, 100)
    elif (sensorval == [0, 1, 1]):
        direction = (100, 50)
    elif (sensorval == [1, 0, 0]):
        saveDirection.lastDir = 0
        direction = (0, 90)
    elif (sensorval == [0, 0, 1]):
        saveDirection.lastDir = 1
        direction = (90, 0)
    elif (sensorval == [1, 0, 1]):
        direction = (0, 0)
    elif (sensorval == [0, 0, 0]):
        if saveDirection.lastDir == 0:
            direction = (-90, 90)
        else:
            direction = (90, -90)
    # print(direction)
    runMotor(direction)


def runMotor(values):
    if (values[0] == 0):
        lMotor.stop()
    else:
        lMotor.start(abs(values[0]))

    if (values[1] == 0):
        rMotor.stop()
    else:
        rMotor.start(abs(values[1]))

    if (values[0] >= 0):
        GPIO.output(lMotorR, 0)
        GPIO.output(lMotorF, 1)
    else:
        GPIO.output(lMotorF, 0)
        GPIO.output(lMotorR, 1)

    if (values[1] >= 0):
        GPIO.output(rMotorR, 0)
        GPIO.output(rMotorF, 1)
    else:
        GPIO.output(rMotorF, 0)
        GPIO.output(rMotorR, 1)


try:
    blinkSign()
    while 1:
        readButtons()
        if (startFlag.started):
            decideSpeed()
        else:
            runMotor((0, 0))
except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()

