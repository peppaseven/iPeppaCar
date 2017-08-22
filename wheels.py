#!/usr/bin/python2
#coding=utf-8
import RPi.GPIO as GPIO
import time
'''
2 L298N control 4 Motors. 
SOC Control GPIO
Front Motor: (Left) 15-ENDA, 31-forward,33-backward   
             (Right)29-ENDB, 35-forward,37-backward
Rear Motor:  (Left) 18-ENDB, 38-forward,40-backward
             (Right)22-ENDA, 36-forward,32-backward   

This is temporary test codes, need define a wheels class.
'''
# GPIOs should move a common file to define.
def init():
    GPIO.setmode(GPIO.BOARD)
    # front motor
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(37, GPIO.OUT)

    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(32, GPIO.OUT)

def reset():
    GPIO.output(15, GPIO.LOW)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)

    GPIO.output(18, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(32, GPIO.LOW)


# front left forward
def front_left_forward():
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.HIGH)
# front right forward
def front_right_forward():
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(37, GPIO.HIGH)

# rear left forward
def rear_left_forward():
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.HIGH)

# rear right forward
def rear_right_forward():
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(36, GPIO.HIGH)
    GPIO.output(32, GPIO.LOW)

def front_left_back():
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)

def front_right_back():
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(37, GPIO.LOW)

def rear_left_back():
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(38, GPIO.HIGH)
    GPIO.output(40, GPIO.LOW)

def rear_right_back():
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(32, GPIO.HIGH)

# forward
def forward():
    reset()
    front_left_forward()
    front_right_forward()
    rear_left_forward()
    rear_right_forward()
# backward
def back():
    reset()
    front_left_back()
    front_right_back()
    rear_left_back()
    rear_right_back()
# move forward with left
def front_left_turn():
    reset()
    front_right_forward()
    rear_right_forward()
    time.sleep(0.3)
    reset()

# move forward with right
def front_right_turn():
    reset()
    front_left_forward()
    rear_left_forward()
    time.sleep(0.3)
    reset()

# move backward with left
def rear_left_turn():
    reset()
    rear_left_back()
    front_left_back()
    time.sleep(0.3)
    reset()
# move backward with right
def rear_right_turn():
    reset()
    rear_right_back()
    front_right_back()
    time.sleep(0.3)
    reset()

# stop motor
def stop():
    reset()


if __name__ == "__main__":
    init()
    reset()
    forward()
    time.sleep(2)
    back()
    time.sleep(2)
    front_left_turn()
    time.sleep(2)
    front_right_turn()
    time.sleep(2)
    rear_left_turn()
    time.sleep(1)
    rear_right_turn()
    stop()
    #must call this when exit
    GPIO.cleanup()