#!/usr/bin/python

# importing modules
import RPi.GPIO as GPIO
import time

# GPIO pin defs
sign1 = 19
sign5 = 26

GPIO.setmode(GPIO.BCM)

gpio_outputs = (sign1, sign5)

GPIO.setup(gpio_outputs, GPIO.OUT)
oneSign = GPIO.PWM(sign1, 400)
fiveSign = GPIO.PWM(sign5, 400)

def cleanupGpio():
    GPIO.cleanup()

try:
    oneSign.start(0)
    fiveSign.start(0)
    while 1:
        for i in range(0, 100, 1):
            oneSign.ChangeDutyCycle(i)
            fiveSign.ChangeDutyCycle(i)
            time.sleep(0.01)

        for j in range(100, 0, -1):
            oneSign.ChangeDutyCycle(j)
            fiveSign.ChangeDutyCycle(j)
            time.sleep(0.01)

except KeyboardInterrupt:
    print("cleanup")
    cleanupGpio()
