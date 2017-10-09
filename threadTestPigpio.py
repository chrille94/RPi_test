#!/usr/bin/python

# importing modules
import pigpio
import time
import threading

sequence = ((0,1),(1,0),(0,1),(1,0),(0,1),(1,0),(0,0),(1,1),(0,0),(1,1),(0,0),(1,1),(0,0))

gpio = pigpio.pi()

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

gpio.set_mode(rMotorPWM, pigpio.OUTPUT)
gpio.set_mode(rMotorF, pigpio.OUTPUT)
gpio.set_mode(rMotorR, pigpio.OUTPUT)
gpio.set_mode(lMotorPWM, pigpio.OUTPUT)
gpio.set_mode(lMotorF, pigpio.OUTPUT)
gpio.set_mode(lMotorR, pigpio.OUTPUT)
gpio.set_mode(sign1, pigpio.OUTPUT)
gpio.set_mode(sign5, pigpio.OUTPUT)

gpio.set_mode(rSensor, pigpio.INPUT)
gpio.set_mode(mSensor, pigpio.INPUT)
gpio.set_mode(lSensor, pigpio.INPUT)
gpio.set_mode(button1, pigpio.INPUT)
gpio.set_mode(button2, pigpio.INPUT)
gpio.set_mode(button3, pigpio.INPUT)

gpio.set_PWM_frequency(rMotorPWM, 60)  # Right motor PWM init @ 200Hz
gpio.set_PWM_frequency(lMotorPWM, 60)  # Left motor PWM init @ 200Hz
gpio.set_PWM_frequency(sign1, 400)
gpio.set_PWM_frequency(sign5, 400)

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
        while 1:
            for i in range(0, len(sequence), 1):
                gpio.write(sign1, sequence[i][0])
                gpio.write(sign5, sequence[i][1])
                time.sleep(0.17)
            # for i in range(20, 255, 5):
            #     gpio.set_PWM_dutycycle(sign1, i)
            #     gpio.set_PWM_dutycycle(sign5, i)
            #     time.sleep(0.02)
            #
            # for j in range(255, 20, -5):
            #     gpio.set_PWM_dutycycle(sign1, j)
            #     gpio.set_PWM_dutycycle(sign5, j)
            #     time.sleep(0.02)


def readButtons():
    startButton = gpio.read(button1)
    stopButton = gpio.read(button3)
    if ((savePress.prev_input1) and not startButton):
        # print("start pressed")
        startFlag.started = 1
    if ((savePress.prev_input2) and not stopButton):
        # print("Stop pressed")
        startFlag.started = 0

    savePress.prev_input1 = startButton
    savePress.prev_input2 = stopButton


def getSensors():
    leftReadings = [0] * 15
    middleReadings = [0] * 15
    rightReadings = [0] * 15
    linereading = [0] * 3
    for i in range(0, 15):
        leftReadings[i] = gpio.read(lSensor)
        middleReadings[i] = gpio.read(mSensor)
        rightReadings[i] = gpio.read(rSensor)
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
        direction = (200, 200)
    elif (sensorval == [1, 1, 0]):
        direction = (100, 200)
    elif (sensorval == [0, 1, 1]):
        direction = (200, 100)
    elif (sensorval == [1, 0, 0]):
        saveDirection.lastDir = 0
        direction = (0, 200)
    elif (sensorval == [0, 0, 1]):
        saveDirection.lastDir = 1
        direction = (200, 0)
    elif (sensorval == [1, 0, 1]):
        direction = (0, 0)
    elif (sensorval == [0, 0, 0]):
        if saveDirection.lastDir == 0:
            direction = (-200, 200)
        else:
            direction = (200, -200)
    # print(direction)
    runMotor(direction)


def runMotor(values):
    gpio.set_PWM_dutycycle(lMotorPWM, (abs(values[0])))
    gpio.set_PWM_dutycycle(rMotorPWM, (abs(values[1])))

    if (values[0] >= 0):
        gpio.write(lMotorR, 0)
        gpio.write(lMotorF, 1)
    else:
        gpio.write(lMotorF, 0)
        gpio.write(lMotorR, 1)

    if (values[1] >= 0):
        gpio.write(rMotorR, 0)
        gpio.write(rMotorF, 1)
    else:
        gpio.write(rMotorF, 0)
        gpio.write(rMotorR, 1)

def resetGpio():
    gpio.write(lMotorF, 0)
    gpio.write(lMotorR, 0)
    gpio.write(rMotorR, 0)
    gpio.write(rMotorF, 0)
    gpio.write(sign1, 0)
    gpio.write(sign5, 0)
    gpio.write(rMotorPWM, 0)
    gpio.write(lMotorPWM, 0)



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
    resetGpio()
    gpio.stop()

