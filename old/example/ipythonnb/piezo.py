import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
'''
for i in range(20):
    print(i)
    GPIO.output(10, GPIO.HIGH)
    time.sleep(.000002)
    GPIO.output(10, GPIO.LOW)
    time.sleep(.000002)
'''

p = GPIO.PWM(10, 2000)
p.start(10)
try:
    while 1:
        for dc in range(1000, 4000, 50):
            p.ChangeFrequency(dc)
            time.sleep(.1)
        for dc in range(4000, 1000, -50):
            p.ChangeFrequency(dc)
            time.sleep(.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
