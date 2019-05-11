import pyzed.sl as sl
import cv2


class Sampler:

    def __init__(self, path, input_mode='default', resolution=sl.RESOLUTION.RESOLUTION_HD720, rectify=True, gray=False):
        """
        The is the constructor for the image sampler
        :param path: the svo file path
        :param input_mode: key word for initial parameter setting. the 'default' is sl.InitParameters(svo_input_filename
        =self.path, svo_real_time_mode=False)
        :param resolution: the resolution for the sampled image, default is HD720
        :param rectify: whether the sample need to be rectified
        :param gray: whether the sample need to be convert to gray scale
        """
        self.path = path
        self.input_mode = input_mode
        self.resolution = resolution
        self.camera = sl.Camera()
        self.rectify = rectify
        self.gray = gray
        self.counter = 1

    def manual_sampling(self, name, path, output_format='image', depth=False, wait_time=1):
        """
        The method to manually sample the image using example code provided by zed. This method would interact with cv2
        to display the image that grabbed by zed camera  The video replay would depend on the computation and the
        waitkey() interval. To sample, just press s and the program would save the current image However, if the path
        if not valid, the program would still think the output succeed.
        :param name: the name for the output files, do not provide .xxx
        :param path: the path for the output files. format /loc/to/put/
        :param output_format: the format of the sample. By default format='image', it will save the sampled image into file.
        format='numpy' will return
        :param depth: whether to output the depth measurement
        :param wait_time: the wait time for the cv2.waitkey() method, default is 1 ms. This setting would effect the
        fps of the replay. To be able to have time to review each frame and decide whether to sample, set up wait_time
        to an appropriate large number such as 3000 which allows roughly 3 seconds to decide whether the current frame
        need to be sampled
        :return: if format='numpy', return a list of sampled data in numpy
        """
        # reset camera and open camera
        self.__new_camera()
        self.__open_camera()

        # set up the runtime params and the mat structure to hold the data
        runtime = sl.RuntimeParameters()
        left = sl.Mat()
        right = sl.Mat()
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
                if self.gray and self.rectify:
                    self.camera.retrieve_image(left, view=sl.VIEW.VIEW_LEFT_GRAY)
                    self.camera.retrieve_image(right, view=sl.VIEW.VIEW_RIGHT_GRAY)
                elif self.gray and not self.rectify:
                    self.camera.retrieve_image(left, view=sl.VIEW.VIEW_LEFT_UNRECTIFIED_GRAY)
                    self.camera.retrieve_image(right, view=sl.VIEW.VIEW_RIGHT_UNRECTIFIED_GRAY)
                elif not self.gray and self.rectify:
                    self.camera.retrieve_image(left, view=sl.VIEW.VIEW_LEFT)
                    self.camera.retrieve_image(right, view=sl.VIEW.VIEW_RIGHT)
                elif not self.gray and not self.rectify:
                    self.camera.retrieve_image(left, view=sl.VIEW.VIEW_LEFT_UNRECTIFIED)
                    self.camera.retrieve_image(right, view=sl.VIEW.VIEW_RIGHT_UNRECTIFIED)
                cv2.imshow("ZED-Left", left.get_data())
                key = cv2.waitKey(wait_time)
                if output_format == 'image':
                    # left
                    l_name = name + '_left'
                    self.__save_image(key, left, l_name, path)
                    # right
                    r_name = name + '_right'
                    self.__save_image(key, right, r_name, path)
                    # depth to left image
                    if depth:
                        depth = sl.Mat()
                        self.camera.retrieve_image(depth, view=sl.VIEW.VIEW_DEPTH)
                        d_name = name + '_depth'
                        self.__save_image(key, depth, d_name, path)
                elif output_format == 'numpy':
                    left_np, right_np = self.__output_numpy(key, left), self.__output_numpy(key, right)
                    left_list.append(left_np)
                    right_list.append(right_np)
                    if depth:
                        depth_mat = sl.Mat()
                        self.camera.retrieve_image(depth_mat, view=sl.VIEW.VIEW_DEPTH)
                        depth_np = self.__output_numpy(key, depth_mat)
                        depth_list.append(depth_np)
                else:
                    print("\nInvalid format attribute. Format should be image or numpy")
                self.counter = self.counter + 1
            else:
                key = cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
        # release the mat and close the camera
        left.free()
        right.free()
        self.camera.close()
        if output_format == 'numpy':
            return left_list, right_list, depth_list

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
            path = path + name + self.counter + ".png"
            mat.write(path)

    @staticmethod
    def __output_numpy(key, mat):
        im_numpy = None
        if key == 115:
            im_numpy = mat.get_data()
        return im_numpy

    def __new_camera(self):
        """
        The method to close the current and create a new camera for sampling
        :return: void
        """
        self.camera = sl.Camera()
        self.counter = 1
        print("\nCreated a new camera, counter reset.\n")

    def __open_camera(self):
        """
        Method to open a
        :return: void
        """
        if self.input_mode == 'default':
            init = sl.InitParameters(svo_input_filename=self.path, svo_real_time_mode=False)
            init.camera_resolution = self.resolution

        # TODO: other input mode e.g real time mode
        # create and open a camera
        print("\nLoading camera...")
        status = self.camera.open(init)
        if status != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
        else:
            print("Camera successfully loaded\n")







