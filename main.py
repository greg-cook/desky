#!/usr/bin/env python

import buttonshim
import redis
import RPi.GPIO as GPIO
import signal
import time

try:
    GPIO.setmode(GPIO.BCM)

    PIN_TRIG = 4
    PIN_ECHO = 17

    GPIO.setup(PIN_TRIG, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIG, False)

    PIN_RELAY_UP = 26
    PIN_RELAY_DN = 20

    GPIO.setup(PIN_RELAY_UP, GPIO.OUT)
    GPIO.setup(PIN_RELAY_DN, GPIO.OUT)

    def desk_stop():
        GPIO.output(PIN_RELAY_UP, True)
        GPIO.output(PIN_RELAY_DN, True)

    def desk_up():
        GPIO.output(PIN_RELAY_UP, False)

    def desk_down():
        GPIO.output(PIN_RELAY_DN, False)

    desk_stop()

    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    current_height = float(0)
    pulse_start_time = float(0)
    pulse_start_time = float(0)

    def get_height():
        global current_height
        global pulse_start_time
        global pulse_start_time
        time.sleep(0.5)
        GPIO.output(PIN_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIG, False)
        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        current_height = round(pulse_duration * 17150, 2)
        print("Current:", current_height, "cm")

    # Allow sensor to settle before measuring the first time
    get_height()

    target_height = 0

    def goto_preset():
        global target_height
        print("Target:", target_height, "cm")
        if current_height > target_height:
            while current_height > target_height:
                desk_down()
                time.sleep(0.1)
                get_height()
            desk_stop()
        elif current_height < target_height:
            while current_height < target_height:
                desk_up()
                time.sleep(0.2)
                get_height()
            desk_stop()

    #########################################################
    #   Button A - used to move desk to preset 1 (seated)   #
    #########################################################

    button_a_held = False

    @buttonshim.on_press(buttonshim.BUTTON_A)
    def button_a_press(button, pressed):
        global button_a_held
        button_a_held = False

    @buttonshim.on_hold(buttonshim.BUTTON_A, hold_time=3)
    def button_a_hold(button):
        global button_a_held
        button_a_held = True
        buttonshim.set_pixel(64, 255, 64)
        get_height()
        r.set("preset_1", current_height)
        time.sleep(3)
        buttonshim.set_pixel(0, 0, 0)

    @buttonshim.on_release(buttonshim.BUTTON_A)
    def button_a_release(button, pressed):
        if not button_a_held:
            global target_height
            target_height = float(r.get("preset_1"))
            goto_preset()

    #########################################################
    #   Button B - used to move desk to preset 2 (standing) #
    #########################################################

    button_b_held = False

    @buttonshim.on_press(buttonshim.BUTTON_B)
    def button_b_press(button, pressed):
        global button_b_held
        button_b_held = False

    @buttonshim.on_hold(buttonshim.BUTTON_B, hold_time=3)
    def button_b_hold(button):
        global button_b_held
        button_b_held = True
        buttonshim.set_pixel(64, 64, 256)
        get_height()
        r.set("preset_2", current_height)
        time.sleep(3)
        buttonshim.set_pixel(0, 0, 0)

    @buttonshim.on_release(buttonshim.BUTTON_B)
    def button_b_release(button, pressed):
        if not button_b_held:
            global target_height
            target_height = float(r.get("preset_2"))
            goto_preset()

    #########################################################
    #   Button D - used to move desk down manually          #
    #########################################################
    @buttonshim.on_press(buttonshim.BUTTON_D)
    def button_d_press(button, pressed):
        desk_down()

    @buttonshim.on_release(buttonshim.BUTTON_D)
    def button_d_release(button, pressed):
        desk_stop()
        time.sleep(2)
        get_height()

    #########################################################
    #   Button E - used to move desk up manually            #
    #########################################################
    @buttonshim.on_press(buttonshim.BUTTON_E)
    def button_e_press(button, pressed):
        desk_up()

    @buttonshim.on_release(buttonshim.BUTTON_E)
    def button_e_release(button, pressed):
        desk_stop()
        time.sleep(2)
        get_height()

    signal.pause()

finally:
    GPIO.cleanup()
