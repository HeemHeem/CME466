"""
CME466 Deliverable 1
Jason Xie
xix277
11255431

"""
import RPi.GPIO as GPIO

BtnPin = 17
Gpin   = 18
Rpin   = 27

on_off = False
tmp = False

def setup():
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    # GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    # GPIO.output(Rpin, GPIO.LOW)    # set led off first
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=detect, bouncetime=50)

def switch():
    global on_off
    # if GPIO.event_detected(BtnPin) and on_off == 0:
    #     on_off = 1
    #     # print("OFF")
    # elif GPIO.event_detected(BtnPin) and on_off == 1:
    #     on_off = 0
        # print("RED")
    if GPIO.event_detected(BtnPin):
        on_off = not on_off

def Print(on_off):
    global tmp
    if on_off != tmp:
        if on_off == False:
            print("OFF")

        if on_off == True:
            print("ON")
        tmp = on_off

def Led(x):
    if x == True:
        GPIO.output(Rpin, GPIO.HIGH)
        # GPIO.output(Gpin, 0)
    if x == False:
        GPIO.output(Rpin, GPIO.LOW)
        # GPIO.output(Gpin, 1)

def detect(chn):
    Led(on_off)

def loop():
    while True:
        switch()
        Print(on_off)

def destroy():
    # GPIO.output(Gpin, GPIO.HIGH)       # Green led off
    GPIO.output(Rpin, GPIO.LOW)       # Red led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
