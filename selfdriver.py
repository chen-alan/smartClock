import numpy as np
import cv2

from mypicar.front_wheels import Front_Wheels
from mypicar.back_wheels import Back_Wheels
from detector_wrapper import DetectorWrapper
from video_capture_async import VideoCaptureAsync
from mypicar import camera
import time

front_wheels = Front_Wheels()
back_wheels = Back_Wheels()

detector = DetectorWrapper()

front_wheels.turn_straight()
cam = camera.Camera(debug=False)
cam.ready()
time.sleep(3)
try:
    # uncomment these two lines to let the car move
    back_wheels.speed = 23
    back_wheels.forward()
    diff = 0
    currangle = 0 # current angle the wheels are turned
    cam.turn_up(5)
    prev_diff = 0
    while True:
        # Capture frame-by-frame
        success, ret = detector.detect()

        if success:
            # uncomment this line to plot lane detection result
            # (only use with a VNC client)
            detector.plot(ret)
            diff = (320-ret[1])/10

            print(diff)
            
            if(diff > 0):
                cam.turn_left(abs(diff/8))
                #if currangle > -2:
                 #  currangle = 0
                currangle = currangle - abs(diff/7)
                if diff-prev_diff > 0:
                    front_wheels.turn_rel(currangle)
                else:
                    print('keep going left', currangle)
                    #front_wheels.turn_straight()
            elif(diff < 0):
                cam.turn_right(abs(diff/8))
                #if currangle < 2:
                 #  currangle = 0
                currangle = currangle + abs(diff/7)
                if diff-prev_diff < 0:
                    front_wheels.turn_rel(currangle)
                else:
                    print('keep going right', currangle)
                    #front_wheels.turn_straight()
            else:
                front_wheels.turn_straight()
                cam.ready()
                cam.turn_up(5)
                currangle = 0
        else:
            currangle = 0
            cam.ready()
            cam.turn_up(5)
            if diff < 0:
                front_wheels.turn_rel(15)
                cam.turn_right(abs(diff))
            else:
                front_wheels.turn_rel(-15)
                cam.turn_left(abs(diff))
        prev_diff = diff 
except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    back_wheels.stop()
    front_wheels.turn_straight()
    detector.stop()
    cam.ready()
