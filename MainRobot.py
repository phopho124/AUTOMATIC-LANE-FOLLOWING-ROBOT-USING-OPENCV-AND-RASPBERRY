from Motor import Motor
from LaneDetect import getLaneCurve
import Webcam
from time import sleep

##################################################
motor = Motor(2, 3, 4, 17, 22, 27)
##################################################

def main():
    img = Webcam.getImg(True)
    curveVal = getLaneCurve(img)

    speed =0.3
    print('Curve = ', curveVal)

    if curveVal > 0:
        if curveVal < 8:
            maxVAl = 0
        elif curveVal < 29:
            maxVAl = 22
        elif curveVal < 35:
            maxVAl = 23
        else:
            maxVAl = 24

    else:
        if curveVal > -8:
            maxVAl = 0
        elif curveVal > -29:
            maxVAl = -22
        elif curveVal > -35:
            maxVAl = -23
        else:
            maxVAl = -24

    print('CurveFi = ', maxVAl)
    motor.move(speed, maxVAl, 0.05)

while True:
    main()