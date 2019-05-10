import pyzed.sl as sl
import cv2


class Sampler:

    def __init__(self, path, input_mode='default'):
        """
        The is the constructor for the image sampler
        :param path: the svo file path
        :param input_mode: key word for initial parameter setting. the 'default' is sl.InitParameters(svo_input_filename
        =self.path, svo_real_time_mode=False)
        """
        self.path = path
        self.input_mode = input_mode
        self.camera = sl.Camera()

    def manual_sampling(self, name, path, wait_time=1):
        """
        The method to manually sample the image using example code provided by zed. This method would interact with cv2
        to display the image that grabbed by zed camera  The video replay would depend on the computation and the
        waitkey() interval. To sample, just press s and the program would save the current image However, if the path
        if not valid, the program would still think the output succeed.
        :param name: the name for the output files
        :param wait_time: the wait time for the cv2.waitkey() method, default is 1 ms. This setting would effect the
        fps of the replay.
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








