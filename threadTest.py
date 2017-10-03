#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time
import threading

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

class runRobot(threading.Thread):
    def __init__(self):
        self.sensorval = []*3
        self.direction = ()
        self.leftReadings = [0] * 15
        self.middleReadings = [0] * 15
        self.rightReadings = [0] * 15
        self.linereading = [0] * 3
        self.values = ()
    def run(self):
        self.sensorval = self.getSensors()
        # print(self.sensorval)
        if (self.sensorval == [1, 1, 1]) or (self.sensorval == [0, 1, 0]):
            self.direction = (100, 100)
        elif (self.sensorval == [1, 1, 0]):
            self.direction = (50, 100)
        elif (self.sensorval == [0, 1, 1]):
            self.direction = (100, 50)
        elif (self.sensorval == [1, 0, 0]):
            #saveself.Direction.lastDir = 0
            self.direction = (0, 90)
        elif (self.sensorval == [0, 0, 1]):
            #saveself.Direction.lastDir = 1
            self.direction = (90, 0)
        elif (self.sensorval == [1, 0, 1]):
            self.direction = (0, 0)
        elif (self.sensorval == [0, 0, 0]):
            self.direction = (-50, -50)
            #if saveself.Direction.lastDir == 0:
            #   self.direction = (-90, 90)
            #else:
            #    self.direction = (90, -90)
        # print(self.direction)
        self.runMotor(self.direction)

    def getSensors(self):

        for i in range(0, 15):
            self.leftReadings[i] = GPIO.input(lSensor)
            self.middleReadings[i] = GPIO.input(mSensor)
            self.rightReadings[i] = GPIO.input(rSensor)
        # self.linereading = [GPIO.input(lSensor), GPIO.input(mSensor), GPIO.input(rSensor)]
        # print(self.linereading)
        if (self.leftReadings.count(1) > 3):
            self.linereading[0] = 1
        else:
            self.linereading[0] = 0

        if (self.middleReadings.count(1) > 3):
            self.linereading[1] = 1
        else:
            self.linereading[1] = 0

        if (self.rightReadings.count(1) > 3):
            self.linereading[2] = 1
        else:
            self.linereading[2] = 0

        # print(self.leftReadings.count(1))
        # print(self.middleReadings.count(1))
        # print(self.rightReadings.count(1))
        # print(self.linereading)

        return self.linereading

    def runMotor(self, values):
        if (self.values[0] == 0):
            lMotor.stop()
        else:
            lMotor.start(abs(values[0]))

        if (self.values[1] == 0):
            rMotor.stop()
        else:
            rMotor.start(abs(values[1]))
        # print(abs(values[0]))
        # print(abs(values[1]))

        if (self.values[0] >= 0):
            GPIO.output(lMotorR, 0)
            GPIO.output(lMotorF, 1)
        else:
            GPIO.output(lMotorF, 0)
            GPIO.output(lMotorR, 1)

        if (self.values[1] >= 0):
            GPIO.output(rMotorR, 0)
            GPIO.output(rMotorF, 1)
        else:
            GPIO.output(rMotorF, 0)
            GPIO.output(rMotorR, 1)



def setSign(numbersToShow):
    GPIO.output(sign1, numbersToShow[0])
    GPIO.output(sign5, numbersToShow[1])





def cleanupGpio():
    GPIO.cleanup()

def blinkSign():
    setSign((0, 1))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)
    setSign((0, 1))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)
    setSign((1, 0))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)
    setSign((1, 0))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)
    setSign((1, 1))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)
    setSign((1, 1))
    time.sleep(0.3)
    setSign((0, 0))
    time.sleep(0.3)

#blinkthread = threading.Thread(target=blinkSign())
#blinkthread.start()

mainThread = runRobot()

try:
    while 1:
        mainThread.start()
            # decideSpeed()
            # setSign((1, 0))
        #else:
            #runMotor((0, 0))
            # setSign((0, 1))
except KeyboardInterrupt:
    print
    "cleanup"
    cleanupGpio()