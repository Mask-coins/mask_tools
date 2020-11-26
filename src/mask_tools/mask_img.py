from PIL import Image
import numpy as np
import math


def image_patch(filepass, patch_size=50):
    '''
    dividing picture into patch
    :param filepass:
    :param patch_size:
    :return: array of patches.
    if you input image:(348,236,3) and path_size=50,
    return numpy.ndarray(7,5,50,50,3)
    '''
    img = np.array(Image.open(filepass))
    print(img.shape)
    height,width,color = img.shape
    w = math.ceil(width/patch_size)*patch_size-width
    h = math.ceil(height/patch_size)*patch_size-height
    img = np.pad(img,((0, h), (0, w), (0, 0)), "constant")
    print(img.shape)
    height,width,color = img.shape
    # https://stackoverflow.com/questions/31527755/extract-blocks-or-patches-from-numpy-array
    img = img.reshape(height//patch_size, patch_size, width//patch_size, patch_size, color)
    img = img.swapaxes(1, 2)
    print(img.shape)
    return img



