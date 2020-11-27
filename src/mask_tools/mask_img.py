from PIL import Image
import numpy as np
import math
from pathlib import Path


def image_patch(img_input, patch_size=50):
    '''
    dividing picture into patch
    :param img_input: array or pass of file.
    :param patch_size:
    :return: array of patches.
    if you input image:(348,236,3) and path_size=50,
    return numpy.ndarray(7,5,50,50,3)
    '''
    if type(img_input)==str or isinstance(img_input, Path):
        img = np.array(Image.open(img_input))
    else:
        img = np.array(img_input)
    if img.ndim == 3:
        height,width,color = img.shape
        w = math.ceil(width/patch_size)*patch_size-width
        h = math.ceil(height/patch_size)*patch_size-height
        img = np.pad(img,((0, h), (0, w), (0, 0)), "constant")
        height,width,color = img.shape
        # https://stackoverflow.com/questions/31527755/extract-blocks-or-patches-from-numpy-array
        img = img.reshape(height//patch_size, patch_size, width//patch_size, patch_size, color)
        img = img.swapaxes(1, 2)
    elif img.ndim == 2:
        height,width = img.shape
        w = math.ceil(width/patch_size)*patch_size-width
        h = math.ceil(height/patch_size)*patch_size-height
        img = np.pad(img,((0, h), (0, w)), "constant")
        height,width = img.shape
        # https://stackoverflow.com/questions/31527755/extract-blocks-or-patches-from-numpy-array
        img = img.reshape(height//patch_size, patch_size, width//patch_size, patch_size)
        img = img.swapaxes(1, 2)
    else:
        raise ValueError("input dimension must be 2 or 3")
    return img



