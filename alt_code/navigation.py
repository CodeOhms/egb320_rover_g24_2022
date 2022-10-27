#Import cool stuff and things
import PiCameraSystem as pcam
import RPi.GPIO as GPIO
from time import sleep
import numpy as np

#SetMode
GPIO.setmode(GPIO.BCM)

#Left Motor Setup
PWM1,IN1,IN2 = 100,22,13 #switch these on the day
GPIO.setup(IN1,GPIO.OUT) #Forwards
GPIO.setup(IN2,GPIO.OUT) #Reverse 
PWMA = GPIO.PWM(IN1,PWM1)
PWMAR = GPIO.PWM(IN2,PWM1)
PWMA.start(0)
PWMAR.start(0)

#Right Motor Setup
PWM2,IN3,IN4 = 100,23,12
GPIO.setup(IN3,GPIO.OUT) #Forwards
GPIO.setup(IN4,GPIO.OUT) #Reverse
PWMB = GPIO.PWM(IN3,PWM2)
PWMBR = GPIO.PWM(IN4,PWM2)
PWMB.start(0)
PWMBR.start(0)

#servo setup
IN5 = 14
GPIO.setup(IN5, GPIO.OUT)
servo = GPIO.PWM(IN5,50)
servo.start(0)    

#sets the speed of the system
setspeed = 40
    
global ball_found
ball_found = False   
while True:
    print(ball_found)
    #Pull data from the vision system
    v = pcam.read()
    
    #If sample is not visable rotate
    if len(v.samples) == 0:
        PWMA.ChangeDutyCycle(setspeed)
        PWMAR.ChangeDutyCycle(0)
        PWMB.ChangeDutyCycle(0)
        PWMBR.ChangeDutyCycle(0)
    #Locate the closest sample
    else:
        # simplify the data
        theta = v.samples[0].bearingx
        depth = v.samples[0].distance

        l_theta = v.landers[0].bearingx
        l_depth = v.landers[0].distance
        
        print(str(theta) + " " + str(depth))
        
        if ball_found == False:
            if theta > 5:
                if theta > 15:
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)            
                    print('hard right')
                else:
                    print('right')
                    PWMA.ChangeDutyCycle(setspeed + 5)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed - 5)
                    PWMBR.ChangeDutyCycle(0)
            elif theta < -5:
                if theta < -15:
                    print('hard left')
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0) 
                else:
                    print('left')
                    PWMA.ChangeDutyCycle(setspeed - 5)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed + 5)
                    PWMBR.ChangeDutyCycle(0)            
            else:
                if depth > 170:
                    print('go')
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0)
                else:
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)
                    servo.ChangeDutyCycle(3)
                    sleep(0.8)
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0)
                    sleep(0.8)
                    servo.ChangeDutyCycle(4.5)
                    sleep(0.3)
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)
                    ball_found = True
        else:
            if l_theta > 5:
                if l_theta > 15:
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)            
                    print('hard right')
                else:
                    print('right')
                    PWMA.ChangeDutyCycle(setspeed + 5)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed - 5)
                    PWMBR.ChangeDutyCycle(0)
            elif l_theta < -5:
                if l_theta < -15:
                    print('hard left')
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0) 
                else:
                    print('left')
                    PWMA.ChangeDutyCycle(setspeed - 5)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed + 5)
                    PWMBR.ChangeDutyCycle(0)            
            else:
                if l_depth > 170:
                    print('go')
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0)
                else:
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)
                    sleep(0.8)
                    PWMA.ChangeDutyCycle(setspeed)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(setspeed)
                    PWMBR.ChangeDutyCycle(0)
                    sleep(1.2)
                    servo.ChangeDutyCycle(3)
                    sleep(0.3)
                    PWMA.ChangeDutyCycle(0)
                    PWMAR.ChangeDutyCycle(0)
                    PWMB.ChangeDutyCycle(0)
                    PWMBR.ChangeDutyCycle(0)
                    ball_found = True
        
          
        
    
