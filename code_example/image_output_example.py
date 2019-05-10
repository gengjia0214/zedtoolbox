import pyzed.sl as sl
import cv2


def main():

    filepath = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo'
    print("Reading SVO file: {0}".format(filepath))

    # initial parameter to feed the camera object
    init = sl.InitParameters(svo_input_filename=filepath, svo_real_time_mode=False)
    # create a camera object
    cam = sl.Camera()
    # open the camera, if the init is to receive a svo file, then it will open a window and play the video
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    # set up runtime parameters
    # this is for grab method, the param will determine what kind of information will be grabbed
    # it will determine the amount of computation
    runtime = sl.RuntimeParameters()
    # mat is a data structure for storing any output image data
    # when.retrieve_image(mat) is called, the mat object will be loaded with the image data
    # use mat.get_data() will return data that can be integrated by cv2
    mat = sl.Mat()

    key = ''
    print("  Save the current image:     s")
    print("  Quit the video reading:     q\n")
    while key != 113:  # for 'q' key
        # grab() will compute the current image and put the data into memory
        # the pointer will proceed one frame after each time this method is called
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            # retrieve_image would put the data of a certain channel into the mat structure
            # default is the left view
            cam.retrieve_image(mat)
            cv2.imshow("ZED", mat.get_data())
            key = cv2.waitKey(10000)
            saving_image(key, mat)
        else:
            key = cv2.waitKey(100)
    cv2.destroyAllWindows()

    # print the camera related information
    print_camera_information(cam)
    saving_depth(cam)
    saving_point_cloud(cam)

    cam.close()
    print("\nFINISH")


def print_camera_information(cam):
    while True:
        res = input("Do you want to display camera information? [y/n]: ")
        if res == "y":
            print()
            print(repr((cam.get_self_calibration_state())))
            print("Distorsion factor of the right cam before calibration: {0}.".format(
                cam.get_camera_information().calibration_parameters_raw.right_cam.disto))
            print("Distorsion factor of the right cam after calibration: {0}.\n".format(
                cam.get_camera_information().calibration_parameters.right_cam.disto))

            print("Confidence threshold: {0}".format(cam.get_confidence_threshold()))
            print("Depth min and max range values: {0}, {1}".format(cam.get_depth_min_range_value(),
                                                                    cam.get_depth_max_range_value()))

            print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
            print("Camera FPS: {0}".format(cam.get_camera_fps()))
            print("Frame count: {0}.\n".format(cam.get_svo_number_of_frames()))
            break
        elif res == "n":
            print("Camera information not displayed.\n")
            break
        else:
            print("Error, please enter [y/n].\n")


def saving_image(key, mat):
    if key == 115:
        img = sl.ERROR_CODE.ERROR_CODE_FAILURE
        while img != sl.ERROR_CODE.SUCCESS:
            filepath = input("Enter filepath name: ")
            # one potential problem here is that if the directory is not correct, it will still tell the user that the
            # output is success
            img = mat.write(filepath)
            print("Saving image : {0}".format(repr(img)))
            if img == sl.ERROR_CODE.SUCCESS:
                break
            else:
                print("Help: you must enter the filepath + filename + PNG extension.")


def saving_depth(cam):
    while True:
        res = input("Do you want to save the depth map? [y/n]: ")
        if res == "y":
            save_depth = 0
            while not save_depth:
                filepath = input("Enter filepath name: ")
                save_depth = sl.save_camera_depth_as(cam, sl.DEPTH_FORMAT.DEPTH_FORMAT_PNG, filepath)
                if save_depth:
                    print("Depth saved.")
                    break
                else:
                    print("Help: you must enter the filepath + filename without extension.")
            break
        elif res == "n":
            print("Depth will not be saved.")
            break
        else:
            print("Error, please enter [y/n].")


def saving_point_cloud(cam):
    while True:
        res = input("Do you want to save the point cloud? [y/n]: ")
        if res == "y":
            save_point_cloud = 0
            while not save_point_cloud:
                filepath = input("Enter filepath name: ")
                save_point_cloud = sl.save_camera_point_cloud_as(cam,
                                                                   sl.POINT_CLOUD_FORMAT.
                                                                   POINT_CLOUD_FORMAT_PCD_ASCII,
                                                                   filepath, True)
                if save_point_cloud:
                    print("Point cloud saved.")
                    break
                else:
                    print("Help: you must enter the filepath + filename without extension.")
            break
        elif res == "n":
            print("Point cloud will not be saved.")
            break
        else:
            print("Error, please enter [y/n].")

if __name__ == "__main__":
    main()