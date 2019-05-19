from zedtoolbox.sampler import Sampler
import cv2
import numpy as np


def main():
    """
    Test
    :return: void
    """
    pass


def test_manual_sampling_1():
    """
    Test manual_sampling() on output image
    :return: void
    """
    path_to_file = 'path'
    s1 = Sampler(path_to_file, depth=True)
    s1.depth = True

    f_name = "yellow"
    path = 'path/to/output'
    s1.manual_sampling(f_name, path)


def test_manual_sampling_2():
    """
    Test manual_sampling() on output np array as in
    :return: void
    """
    path_to_file = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo'
    s1 = Sampler(path_to_file, depth=True)
    f_name = "yellow"
    path_array = '/home/jgeng/Documents/Multi-Platform/JIA/Git/zedtoolbox/output/array/'
    s1.manual_sampling(f_name, path_array, output_format='matrix_file')
    # show image
    cv2.waitKey()


# execute the test
if __name__ == "__main__":
    main()


