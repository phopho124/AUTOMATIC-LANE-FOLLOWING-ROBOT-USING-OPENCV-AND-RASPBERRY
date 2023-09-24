import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA, GPIO.OUT);
        GPIO.setup(self.In1A, GPIO.OUT);
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT);
        GPIO.setup(self.In1B, GPIO.OUT);
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 200);
        self.pwmB = GPIO.PWM(self.EnaB, 200);
        self.pwmA.start(0);
        self.pwmB.start(0);
        self.mySpeed = 0

    def move(self, speed=0.5, turn=0, t=0):
        #delay = 0.5

        sp = turn * 2 #t
        s = turn * 0.8
        
        if sp > 0:
            leftSpeed = sp
            rightSpeed = sp/4
            #sleep(delay)
            
        elif s < 0:
            leftSpeed = s/0.5
            rightSpeed = s
            #sleep(delay)
        else:
            leftSpeed = speed * 145
            rightSpeed = speed * 60

        print('Left = ', leftSpeed)
        print('Right = ', rightSpeed)

        self.pwmA.ChangeDutyCycle(abs(rightSpeed))
        self.pwmB.ChangeDutyCycle(abs(leftSpeed))

        GPIO.output(self.In1B, GPIO.HIGH);GPIO.output(self.In2B ,GPIO.LOW)
        GPIO.output(self.In1A, GPIO.HIGH);GPIO.output(self.In2A, GPIO.LOW)
       
        sleep(t)


    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        self.mySpeed = 0
        #sleep(delay)
        sleep(t)
