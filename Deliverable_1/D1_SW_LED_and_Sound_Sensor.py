"""
CME466 Deliverable 1
Jason Xie
xix277
11255431

"""
import PCF8591 as ADC
import RPi.GPIO as GPIO
# import threading
# import time

BtnPin = 17
Gpin   = 18
Rpin   = 27

on_off = False
tmp = False
count = 0
red_green = False
sound_detected = False

def setup():
    ADC.setup(0x48)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.output(Rpin, GPIO.LOW)    # turn red led off
    GPIO.output(Gpin, GPIO.LOW)    # turn green led off
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    # GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=detect, bouncetime=50)
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, bouncetime=300)



def switch():
    """
    Turn the system on or off upon button press

    """
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
    """
    Display whether the system is on or off based on the on_off boolean.

    on_off: True for on, False for off

    """
    global tmp
    if on_off != tmp:
        if on_off == False:
            print("OFF")

        if on_off == True:
            print("ON")
        tmp = on_off

def Led():
    """
    Change Led Colour based on sound input.
    If red_green is True, the LED will be red. If red_green is False, the LED will be Green.
    If on_off is True, the LED is on. If on_off is False, the LED is off 
    """

    global on_off
    global red_green
    # global sound_detected
    if on_off == True:
        

        # if sound_detected:

        if red_green: # red led
            GPIO.output(Rpin, GPIO.HIGH)
            GPIO.output(Gpin, GPIO.LOW)
        
        if not red_green: # green led
            GPIO.output(Rpin, GPIO.LOW)
            GPIO.output(Gpin, GPIO.HIGH)

        # GPIO.output(Gpin, 0)
    if on_off == False:
        GPIO.output(Rpin, GPIO.LOW)
        GPIO.output(Gpin, GPIO.LOW)

def detect():
    """
    Runs the LED function.

    """
    # Redundant, could just take it out after, but might keep it in case of using events and multithreading
    Led()
    # change_color_with_sound()

def print_color(rg):
    """
    Prints what colour the LED is currently.
    If rg is True, the LED is red. Otherwise the LED is green
    """
    if rg:
        print("LIGHT IS NOW RED")
    else:
        print("LIGHT IS NOW GREEN")

def change_color_with_sound():
    """
    Changes the LED colour to either green or red upon detecting a sound value less than 75. Prints the sound value
    and a counter of how many times it has been activied.
    Upon detecting sound, it will change the red_green boolean and increase the counter of how many times it has been activated
    """

    global count
    global red_green
    global sound_detected
    sound_detected = False
    voiceValue = ADC.read(0)
    # if voiceValue:
        # print ("Value:", voiceValue)
    if on_off:
        if voiceValue < 75:
            print ("Value:", voiceValue)
            print ("Voice In!! ", count)
            sound_detected = True
            red_green = not red_green
            print_color(red_green)
            count += 1
    # time.sleep(1)

def loop():
    while True:
        switch()
        detect()
        change_color_with_sound()
        Print(on_off)



def destroy():
    GPIO.output(Gpin, GPIO.LOW)       # Green led off
    GPIO.output(Rpin, GPIO.LOW)       # Red led off
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
