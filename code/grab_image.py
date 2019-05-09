import pyzed.sl as sl
import numpy as np
import cv2 as cv


filepath = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo';
init = sl.InitParameters(svo_input_filename=filepath, svo_real_time_mode=False)
cam = sl.Camera()
status = cam.open(init)
if status != sl.ERROR_CODE.SUCCESS:
    print("fail")
    exit()


