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


class ImageRegistrationSet:

    # reference image for this set
    reference = None

    # images to align with reference image
    images = []

    def __init__(self):
        pass

    """
    Sets reference image.
    @param ref: reference image to set with
    """
    def set_reference(self, ref):
        self.reference = ref


    """
    Gets reference image.
    @return: reference image
    """
    def get_reference(sef):
        return self.reference


    """
    Adds a new image to the set of images.
    @param image: new image to add
    """
    def add_image(self, image):
        self.images.append(image)


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
            image = cv2.imread(file_path + file)

            # determine where to sort the image
            if file_name == "reference":
                image_set.set_reference(image)
            else:
                image_set.add_image(image)


if __name__ == "__main__":
    main()
