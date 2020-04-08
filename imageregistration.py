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

from datetime import datetime

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
    Getter for keypoints.
    @return: keypoints
    """
    def get_keypoints(self):
        return self.__keypoints

    """
    Setter for descriptors.
    @param descriptors: descriptors
    """
    def set_descriptors(self, descriptors):
        self.__descriptors = descriptors


    """
    Getter for descriptors.
    @return: descriptors
    """
    def get_descriptors(self):
        return self.__descriptors

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
        return self.__grayscale


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

    """
    Returns the dimension of this image.
    @param heightFirst: if true, height will be the first element of the returned 2-tuple
    @return: 2-tuple representing the 2D dimensions of this image
    """
    def get_size(self, heightFirst = True):
        if (heightFirst):
            return (self.__height, self.__width)
        else:
            return (self.__width, self.__height)
    

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

    orb_detector_features = 5000

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
            image_grayscaled = cv2.cvtColor(image_colored, cv2.COLOR_BGR2GRAY)
            height, width = image_grayscaled.shape
            image = ImageData(image_colored, image_grayscaled, height, width)

            # determine where to sort the image
            if file_name == "reference":
                image_set.set_reference(image)
            else:
                image_set.add_image(image)


    # create ORB detector
    orb_detector = cv2.ORB_create(orb_detector_features)

    ## find keypoints and descriptors (without masks)

    # reference image
    reference =  image_set.get_reference()
    reference_grayscaled = reference.get_grayscaled()
    reference_keypoints, reference_descriptors = orb_detector.detectAndCompute(reference_grayscaled, None)
    reference.set_keypoints(reference_keypoints)
    reference.set_descriptors(reference_descriptors)
    
    # all other images
    for image in image_set.get_images():
        image_grayscaled = image.get_grayscaled()
        image_keypoints, image_descriptors = orb_detector.detectAndCompute(image_grayscaled, None)
        image.set_keypoints(image_keypoints)
        image.set_descriptors(image_descriptors)

    # create a Brute Force Matcher which uses the Hamming distance metric as a measurement mode
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    # match descriptors between an ImageRegistrationSet's reference image and set of images
    matches = []
    for image in image_set.get_images():
        image_descriptors = image.get_descriptors()
        match = matcher.match(reference_descriptors, image_descriptors)
        match.sort(key = lambda x : x.distance)
        matches.append(match)

    # continue with top 90% of matches
    for idx in range(len(matches)):
        match = matches[idx]
        matches[idx] = match[:len(matches)*90]

    # initialize matrices for each image
    matrices = []
    for i in range(len(matches)):

        # get image and its keypoints
        image = image_set.get_images()[i]
        image_keypoints = image.get_keypoints()

        # get image's corresponding match
        # TODO: match should probably be stored in the ImageData class
        match = matches[i]
        match_count = len(match)
        
        # initialize and populate the matrices
        p1 = np.zeros((match_count, 2))
        p2 = np.zeros((match_count, 2))
    
        for j in range(match_count):
            p1[i, :] = image_keypoints[match[j].queryIdx].pt
            p2[i, :] = reference_keypoints[match[j].queryIdx].pt

        matrices.append((p1, p2))

    # find the homography matrices and masks
    homographies = []
    masks = []

    for matrix in matrices:
        homography, mask = cv2.findHomography(matrix[0], matrix[1], cv2.RANSAC)
        homographies.append(homography)
        masks.append(mask)

    # use the homography matrices to transform all non-reference images
    transformations = []
    
    images = image_set.get_images()
    for i in range(len(images)):
        # args for transforming
        image = images[i]
        image_colored = image.get_colored()
        image_dimensions = image.get_size(False)
        homography = homographies[i]

        # transform image
        transformed_image = cv2.warpPerspective(image_colored, homography, image_dimensions)
        transformations.append(transformed_image)
        

    # output transformations
    for transformation_index in range(len(transformations)):

        transformation = transformations[transformation_index]

        file_appendix = now.strftime("%Y%m%d%H%M%S")
        filename = "img_" + file_appendix + ".jpg"
        filepath = "./output/" + filename
        
        cv2.imwrite(filepath, transformation)

        print("Created " + filepath)
    
if __name__ == "__main__":
    main()
