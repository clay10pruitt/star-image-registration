"""
:file: imageregistration.py
:author: clayton pruitt
:date: 4/2/2020
:desc: Computes image registration for all photos in a given directory.
"""


import cv2
import numpy as np
import os, os.path
import sys


##################################
# CLASSES
##################################

class ImageData:
    """
    An assortment of data for an image.
    """

    # colored version of image
    __color = None

    # grayscaled version of image
    __grayscale = None

    # size info
    __height = 0
    __width = 0

    # keypoints and descriptors
    __keypoints = None
    __descriptors = None


    """
    Constructor. Initializes this Image object with a colored and grayscaled version of the same image.
    @param color: image with color
    @param grayscale: image with grayscale
    @param height: height of image
    @param width: width of image
    """
    def __init__(self, color, grayscale, height, width):
        self.__color = color
        self.__grayscale = grayscale
        self.__height = height
        self.__width = width


    """
    Setter for keypoints.
    @param keypoints: keypoints
    """
    def set_keypoints(self, keypoints):
        self.__keypoints = keypoints


    """
    Setter for descriptors.
    @param descriptors: descriptors
    """
    def set_descriptors(self, descriptors):
        self.__descriptors = descriptors


    """
    Getter for the colored image.
    @return: the colored image
    """
    def get_colored(self):
        return self.__color


    """
    Getter for the grayscaled image.
    @return: the grayscaled imaeg
    """
    def get_grayscaled(self):
        return self.__grayscaled


    """
    Getter for image's height.
    @return: height of image
    """
    def get_height(self):
        return self.__height


    """
    Getter for image's width.
    @return: width of image
    """
    def get_width(self):
        return self.__width
    

class ImageRegistrationSet:
    """
    A set of images to be registered against some reference image.
    """

    # reference image for this set
    __reference = None

    # images to align with reference image
    __images = []

    def __init__(self):
        pass

    """
    Sets reference image.
    @param ref: reference image to set with
    """
    def set_reference(self, ref):
        self.__reference = ref


    """
    Gets reference image.
    @return: reference image
    """
    def get_reference(self):
        return self.__reference


    """
    Adds a new image to the set of images.
    @param image: new image to add
    """
    def add_image(self, image):
        self.__images.append(image)



    """
    Gets images to be aligned.
    @return: images
    """
    def get_images(self):
        return self.__images


##################################
# METHODS
##################################


"""
Helper method for main(). Returns a file_path and all files in the path.
@param argv: arguments from command line
@return: 2-tuple containing the file_path and a list of all files in the path
"""
def __parse_input(argv):
    # get directory
    if (len(argv) == 1):
        file_path = input("directory > ")
    else:
        file_path = argv[1]

    # clean input
    if (file_path[:2] != "./"):
        file_path = "./" + file_path

    if (file_path[-1] != "/"):
        file_path = file_path + "/"

    # get file path
    try:
        files_in_path = os.listdir(file_path)
    except FileNotFoundError:
        print("Invalid directory given.")
        print("Terminating program.")
        sys.exit()

    return file_path, files_in_path


"""
Main method.
"""
def main():

    #TODO: Should be able to read images from all subdirectories in the given directory.

    # get all the images from the directory

    image_set = ImageRegistrationSet()

    valid_extensions = [".jpg"]

    file_path, files_in_path = __parse_input(sys.argv)

    for file in files_in_path:

        # get file name (without extension) and file extension
        file_name = os.path.splitext(file)[0].lower()
        file_extension = os.path.splitext(file)[1].lower()

        # only add image if it contains a valid extension
        if file_extension in valid_extensions:

            # read the image into OpenCV2
            image_colored = cv2.imread(file_path + file)
            image_grayscaled = cv2.cvtColor(image_colord, cv2.COLOR_BGR2GRAY)
            height, width = image_colored.shape
            image = ImageData(image_colored, image_grayscaled, height, width)

            # determine where to sort the image
            if file_name == "reference":
                image_set.set_reference(image)
            else:
                image_set.add_image(image)
        
        
if __name__ == "__main__":
    main()
