"""
CME466 Deliverable 1
Jason Xie
xix277
11255431

"""
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def setup():
    ADC.setup(0x48)

def loop():
    count = 0
    while True:
        voiceValue = ADC.read(0)
        if voiceValue:
            print ("Value:", voiceValue)
            if voiceValue < 100:
                print ("Voice In!! ", count)
                count += 1
            time.sleep(0.5)

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        pass