from zedtoolbox.sampler import Sampler
import cv2

path = '/media/jgeng/hd1/CobiaSwimmingData/UMEH_111718/Cobia1-Yellow/Yellow.svo'
s1 = Sampler(path)

f_name = "yellow"
path = "/home/jgeng/Desktop/"

s1.manual_sampling(f_name, path, depth=True)





