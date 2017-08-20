import RPi.GPIO as GPIO
import os
import time
import atexit
import sys
from subprocess import call
import configure


def setup():   
	GPIO.setup(TRIG[0],GPIO.OUT)
	GPIO.setup(ECHO[0],GPIO.IN)
	GPIO.output(TRIG[0], False)

	print "Waiting For Sensor To Settle"


if ('CTRIG' in configure.data):
    TRIG = [int(configure.data['CTRIG'])]            
    ECHO = [int(configure.data['CECHO'])]

    GPIO.setmode(GPIO.BCM)
    setup()

def turnOffGPIO():
	GPIO.cleanup()

atexit.register(turnOffGPIO)
		

def raw_distance(TRIG, ECHO):
    #check a sonar with trigger argv1 and echo argv2
    #example usage
    #python sonar.py 4 17

    # recommended for auto-disabling motors on shutdown!
    GPIO.setmode(GPIO.BCM)
    
        
    print "Distance Measurement In Progress"
    
    GPIO.setup(TRIG,GPIO.OUT)
    
    GPIO.setup(ECHO,GPIO.IN)
    
    GPIO.output(TRIG, False)

    print "Waiting For Sensor To Settle"
    
    time.sleep(2)
    
    GPIO.output(TRIG, True)
    
    time.sleep(0.00001)
    
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
            
    pulse_duration = pulse_end - pulse_start
            
    distance = pulse_duration * 17150
            
    distance = round(distance, 2)
    
    print "Distance:",distance,"cm"
                                            

def distance():
#    print "Distance Measurement In Progress"

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    pulse_end = 0;
    pulse_start = 0;
    
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        
    if (pulse_end == 0 or pulse_start==0):
        return 1000
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance:",distance,"cm"

    return distance


def cdist():
	return distance()


if __name__ == "__main__":
    TRIG = int(sys.argv[1])
    
    ECHO = int(sys.argv[2])
    raw_distance(TRIG, ECHO)
    cdist()
