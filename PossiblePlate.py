# PossiblePlate.py

import cv2
import numpy as np

###################################################################################################
class PossiblePlate:

    # constructor #################################################################################
    def __init__(self):
        self.imgPlate = None
        self.imgGrayscale = None
        self.imgThresh = None

        self.imgInverseThresh = None
        self.listChars = None

        self.rrLocationOfPlateInScene = None


        self.strChars = ""
    # end constructor

# end class




