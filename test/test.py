from zedtoolbox.sampler import Sampler
import cv2


def main():
    """
    Test
    :return: void
    """
    test_manual_sampling_2()

    pass


def test_manual_sampling_1():
    """
    Test manual_sampling() on output image
    :return: void
    """
    path = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo'
    s1 = Sampler(path)
    f_name = "yellow"
    path = "/home/jgeng/Desktop/"
    s1.manual_sampling(f_name, path, depth=True)


def test_manual_sampling_2():
    """
    Test manual_sampling() on output np array
    :return: void
    """
    path = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo'
    s1 = Sampler(path)
    f_name = "yellow"
    path = "/home/jgeng/Desktop/"
    left, right, depth = s1.manual_sampling(f_name, path, depth=True, output_format='numpy')
    # image size
    print(left[0].shape)
    # show image
    cv2.waitKey()


# execute the test
if __name__ == "__main__":
    main()


