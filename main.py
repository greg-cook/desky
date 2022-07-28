import RPi.GPIO as GPIO
import buttonshim
import signal
import time
from datetime import datetime, timezone, timedelta

# Map relays to GPIO pins
relay1 = 26
relay2 = 20
relay3 = 21

# Setup GPIO to control relays
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1,GPIO.OUT)
GPIO.setup(relay2,GPIO.OUT)
GPIO.setup(relay3,GPIO.OUT)

# Default relay state (active-low)
GPIO.output(relay1,True)
GPIO.output(relay2,True)
GPIO.output(relay3,True)

# Button Shim definitions

# Ensure hold state is set to False
# button_a_held = False
button_b_held = False
button_c_held = False
button_d_held = False
button_e_held = False

# Button A - used to move desk up manually
# - button is held to move desk up, we don't need to implement an explicit hold
#   as the action we want to perform requires keeping the button pressed
@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a_press(button, pressed):
    # global button_a_held
    # button_a_held = False
    buttonshim.set_pixel(255, 0, 0)
    GPIO.output(relay1,False)
    print(datetime.now(),"- Desk up started.")

@buttonshim.on_release(buttonshim.BUTTON_A)
def button_a_release(button, pressed):
    # if not button_a_held:
    #     print("Button A: Short press.")
    GPIO.output(relay1,True)
    buttonshim.set_pixel(0, 0, 0)
    print(datetime.now(),"- Desk up ended.")

# @buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=1)
# def button_a_hold(button):
#     global button_a_held
#     button_a_held = True

# Button B - used to move desk down manually
# - button is held to move desk down, we don't need to implement an explicit hold
#   as the action we want to perform requires keeping the button pressed
@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b_press(button, pressed):
    # global button_b_held
    # button_b_held = False
    buttonshim.set_pixel(0, 255, 0)
    GPIO.output(relay2,False)
    print(datetime.now(),"- Desk down started.")

@buttonshim.on_release(buttonshim.BUTTON_B)
def button_b_release(button, pressed):
    # if not button_b_held:
    #     print("Button B: Short press.")
    GPIO.output(relay2,True)
    buttonshim.set_pixel(0, 0, 0)
    print(datetime.now(),"- Desk down ended.")

# Button C - used to move desk to seated height
# Button D - used to move desk to standing height
# Button E - used to make desk dance

try:
    while True:
        signal.pause()

except  KeyboardInterrupt:
    pass

print("cleanup the things")
GPIO.cleanup()
