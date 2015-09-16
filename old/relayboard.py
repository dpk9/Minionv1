import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pinList = [2, 3, 4, 17, 27, 22, 10, 9]

for i in pinList:
    print(i)
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

sleep = 1

GPIO.output(pinList[0], GPIO.LOW)
print 'one'
time.sleep(sleep)
GPIO.output(pinList[0], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[1], GPIO.LOW)
print 'two'
time.sleep(sleep)
GPIO.output(pinList[1], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[2], GPIO.LOW)
print 'three'
time.sleep(sleep)
GPIO.output(pinList[2], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[3], GPIO.LOW)
print 'four'
time.sleep(sleep)
GPIO.output(pinList[3], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[4], GPIO.LOW)
print 'five'
time.sleep(sleep)
GPIO.output(pinList[4], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[5], GPIO.LOW)
print 'six'
time.sleep(sleep)
GPIO.output(pinList[5], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[6], GPIO.LOW)
print 'seven'
time.sleep(sleep)
GPIO.output(pinList[6], GPIO.HIGH)
time.sleep(sleep)

GPIO.output(pinList[7], GPIO.LOW)
print 'eight'
time.sleep(sleep)
GPIO.output(pinList[7], GPIO.HIGH)
time.sleep(sleep)


GPIO.cleanup()
