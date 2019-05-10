import pyzed.sl as sl
import cv2


class Sampler:

    def __init__(self, path, input_mode='default'):
        """
        The is the constructor for the image sampler
        :param path: the svo file path
        :param input_mode: key word for initial parameter setting. the 'default' is
        sl.InitParameters(svo_input_filename=self.path, svo_real_time_mode=False)
        """
        self.path = path
        self.input_mode = input_mode
        self.camera = sl.Camera()

    def manual_sampling(self):
        """
        The method to manually sample the image. The code is from zed examples
        :return: void
        """

    def new_camera(self):
        """
        The method to close the current and create a new camera for sampling
        :return: void
        """
        self.camera.close()
        self.camera = sl.Camera()
        print("\nCreated a new camera.\n")

    def __open_camera(self):
        """
        Method to open a
        :return: false if the camera can not be opened; true if the camera is successfully loaded
        """
        if self.input_mode == 'default':
            init = sl.InitParameters(svo_input_filename=self.path, svo_real_time_mode=False)
        # TODO: other input mode e.g real time mode
        # create and open a camera
        print("\nLoading camera...")
        status = self.camera.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            return False
        else:
            print("Camera successfully loaded\n")
            return True





