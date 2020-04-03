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
    images = []
    valid_extensions = [".jpg"]
    file_path, files_in_path = __parse_input(sys.argv)
    for file_name in files_in_path:
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension in valid_extensions:
            print("file_name: " + file_path + file_name)
            image = cv2.imread(file_path + file_name)
            images.append(image)

    print("Found following files: " + str(images))


if __name__ == "__main__":
    main()
