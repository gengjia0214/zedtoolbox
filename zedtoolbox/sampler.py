import pyzed.sl as sl
import cv2
import numpy as np


class Sampler:

    def __init__(self, input_mode='default', rectify=True, gray=False, depth=True):
        """
        The is the constructor for the sampler
        :param path: the svo file path
        :param input_mode: key word for initial parameter setting. the 'default' is sl.InitParameters(svo_input_filename
        =self.path, svo_real_time_mode=False)
        :param resolution: the resolution for the sampled image, default is HD720
        :param rectify: whether the sample need to be rectified
        :param gray: whether the sample need to be convert to gray scale
        """
        self.input_mode = input_mode
        self.camera = sl.Camera()
        self.rectify = rectify
        self.gray = gray
        self.counter = 1
        self.depth = depth
        self.left_view = None
        self.right_view = None
        self.set_view()

    def grab_depth_by_timestamps(self, svo_path, out_path, timestamps, fram_rate=30, depth_mode='ultra')

        # load svo file and configurations
        self.__new_camera()
        self.__open_camera(svo_path, depth_mode=depth_mode)
        runtime = sl.RuntimeParameters()

        left_mat = sl.Mat()
        depth_mat = sl.Mat()





    def set_view(self):
        if self.gray and self.rectify:
            self.left_view = sl.VIEW.VIEW_LEFT_GRAY
            self.right_view = sl.VIEW.VIEW_RIGHT_GRAY
        elif self.gray and not self.rectify:
            self.left_view = sl.VIEW.VIEW_LEFT_UNRECTIFIED_GRAY
            self.right_view = sl.VIEW.VIEW_RIGHT_UNRECTIFIED_GRAY
        elif not self.gray and self.rectify:
            self.left_view = sl.VIEW.VIEW_LEFT
            self.right_view = sl.VIEW.VIEW_RIGHT
        elif not self.gray and not self.rectify:
            self.left_view = sl.VIEW.VIEW_LEFT_UNRECTIFIED
            self.right_view = sl.VIEW.VIEW_RIGHT_UNRECTIFIED

    def manual_sampling(self, svo_path, name, path, output_format='image', wait_time=1):
        """
        The method to manually sample the image using example code provided by zed. This method would interact with cv2
        to display the image that grabbed by zed camera  The video replay would depend on the computation and the
        waitkey() interval. To sample, just press s and the program would save the current image However, if the path
        if not valid, the program would still think the output succeed.
        :param name: the name for the output files, do not provide .xxx
        :param path: the path for the output files. format /loc/to/put/
        :param output_format: the format of the sample. By default format='image', it will save the sampled image into
        file. format='matrix' will return a tuple of lists of numpy array. format = 'matrix_file' will save the numpy
        array as file
        :param wait_time: the wait time for the cv2.waitkey() method, default is 1 ms. This setting would effect the
        fps of the replay. To be able to have time to review each frame and decide whether to sample, set up wait_time
        to an appropriate large number such as 3000 which allows roughly 3 seconds to decide whether the current frame
        need to be sampled
        :return: if format='numpy', return a list of sampled data in numpy
        """
        # reset camera and open camera
        self.__new_camera()
        self.__open_camera(svo_path)

        # set up the runtime params and the mat structure to hold the data
        runtime = sl.RuntimeParameters()
        left_mat = sl.Mat()
        right_mat = sl.Mat()
        depth_mat = None
        left_list = list()
        right_list = list()
        depth_list = list()
        # start the sampling loop
        key = ''
        print("  Save the current image:     s")
        print("  Quit the video reading:     q\n")
        while key != 113:  # for 'q' key
            # grab() will compute the current image and put the data into memory
            # the pointer will proceed one frame after each time this method is called
            err = self.camera.grab(runtime)
            if err == sl.ERROR_CODE.SUCCESS:
                # retrieve_image would put the data into the mat structures
                self.camera.retrieve_image(left_mat, view=self.left_view)
                self.camera.retrieve_image(right_mat, view=self.right_view)
                cv2.imshow("ZED-Left", left_mat.get_data())
                key = cv2.waitKey(wait_time)
                if output_format == 'image':
                    # left
                    if key == 115:
                        self.counter = self.counter + 1
                    l_name = name + '_left'
                    self.__save_image(key, left_mat, l_name, path)
                    # right
                    r_name = name + '_right'
                    self.__save_image(key, right_mat, r_name, path)
                    # depth to left image
                    if self.depth:
                        depth_mat = sl.Mat()
                        self.camera.retrieve_image(depth_mat, view=sl.VIEW.VIEW_DEPTH)
                        d_name = name + '_depth'
                        self.__save_image(key, depth_mat, d_name, path)
                else:
                    self.__to_numpy(key, left_mat, left_list)
                    self.__to_numpy(key, right_mat, right_list)
                    if self.depth:
                        depth_mat = sl.Mat()
                        self.camera.retrieve_image(depth_mat, view=sl.VIEW.VIEW_DEPTH)
                        self.__to_numpy(key, depth_mat, depth_list)
            else:
                key = cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
        # release the mat and close the camera
        left_mat.free(memory_type=sl.MEM.MEM_CPU)
        left_mat.free(memory_type=sl.MEM.MEM_GPU)
        right_mat.free(memory_type=sl.MEM.MEM_CPU)
        right_mat.free(memory_type=sl.MEM.MEM_GPU)
        if depth_mat is not None:
            depth_mat.free(memory_type=sl.MEM.MEM_CPU)
            depth_mat.free(memory_type=sl.MEM.MEM_GPU)
        self.camera.close()
        if output_format == 'matrix':
            return left_list, right_list, depth_list
        elif output_format == 'matrix_file':
            l_name = name + "_left"
            r_name = name + "_right"
            d_name = name + "_depth"
            self.__numpy_to_file(left_list, l_name, path)
            self.__numpy_to_file(right_list, r_name, path)
            if self.depth:
                self.__numpy_to_file(depth_list, d_name, path)

    def __save_image(self, key, mat, name, path):
        """
        Method to save the sampled image into png file
        :param key: sensor
        :param mat: mat structure
        :param name: name of the file
        :param path: path for saving the file
        :return: void
        """
        if key == 115:
            path = path + name + str(self.counter) + ".png"
            mat.write(path)

    @staticmethod
    def __to_numpy(key, mat, container):
        """
        Method to output the sample as numpy array
        :param key: sensor
        :param mat: the mat data
        :return: numpy array
        """
        if key == 115:
            im_numpy = mat.get_data()
            container.append(im_numpy)

    @staticmethod
    def __numpy_to_file(arr_list, name, path):
        """
        Method to save a list of numpy array to npy files
        :param arr_list: input array list
        :param name: the name of the file
        :param path: path for ouput
        :return: void
        """
        for num, arr in enumerate(arr_list):
            path_left = path + name + str(num)
            np.save(path_left, arr)

    def __new_camera(self):
        """
        The method to close the current and create a new camera for sampling
        :return: void
        """
        self.camera = sl.Camera()
        self.counter = 1
        print("\nCreated a new camera, counter reset.\n")

    def __open_camera(self, svo_path, depth_mode):
        """
        Method to open a
        :return: void
        """
        if self.input_mode == 'default':
            init = sl.InitParameters()
            init.svo_input_filename = svo_path
            init.svo_real_time_mode = False
            init.camera_resolution = self.resolution
            if depth_mode == 'performance':
                init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE
            if depth_mode == 'medium':
                init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_MEDIUM
            if depth_mode == 'quality':
                init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_QUALITY
            if depth_mode == 'ultra':
                init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_ULTRA

        # TODO: other input mode e.g real time mode
        # create and open a camera
        print("\nLoading camera...")
        status = self.camera.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
        else:
            print("Camera successfully loaded\n")



