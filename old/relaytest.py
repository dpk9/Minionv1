import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class TempControlUnit():
    def __init__(self, r1pin, r2pin, spin):

        self.r1pin = r1pin
        self.r2pin = r2pin
        self.spin = spin

        GPIO.setup(r1pin, GPIO.OUT)
        GPIO.output(r1pin, GPIO.HIGH)

        GPIO.setup(r2pin, GPIO.OUT)
        GPIO.output(r2pin, GPIO.HIGH)

    def onHot(self):

        GPIO.output(self.r1pin, False)
        GPIO.output(self.r2pin, True)

    def onCold(self):

        GPIO.output(self.r1pin, True)
        GPIO.output(self.r2pin, False)

    def onHold(self):

        GPIO.output(self.r1pin, True)
        GPIO.output(self.r2pin, True)

    def test(self):
        self.onHot()
        time.sleep(1)
        self.onCold()
        time.sleep(1)
        self.onHold()
        time.sleep(1)
        self.onHot()
        time.sleep(1)
        self.onHold()
        time.sleep(1)
        self.onCold()
        time.sleep(1)
        self.onHold()


class TempControl():
    def __init__(self):

        self.rPinList = [2, 3, 4, 17, 27, 22, 10, 9]

        self.unitList = []

        self.unitList.append(TempControlUnit(self.rPinList[0], self.rPinList[1], 0))
        self.unitList.append(TempControlUnit(self.rPinList[2], self.rPinList[3], 0))
        self.unitList.append(TempControlUnit(self.rPinList[4], self.rPinList[5], 0))
        self.unitList.append(TempControlUnit(self.rPinList[6], self.rPinList[7], 0))

        self.unitList[0].onHot()
        time.sleep(1)
        self.unitList[1].onHot()
        time.sleep(1)
        self.unitList[2].onCold()
        time.sleep(1)
        self.unitList[3].test()


TempControl()
GPIO.cleanup()


