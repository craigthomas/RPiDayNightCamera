#!/usr/bin/env python
'''
Copyright (C) 2014 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

Simple application to compute the color histogram of the supplied image.
'''
# I M P O R T S ###############################################################

import argparse, cv2, os, sys, logging

from numpy import squeeze, asarray
from matplotlib import pyplot

# C O N S T A N T S ###########################################################

RED = "red"
GREEN = "green"
BLUE = "blue"

# F U N C T I O N S ###########################################################

def parse_arguments():
    '''
    Parses the command line arguments passed to the program.

    @retuyrn a named tuple containing the parsed arguments
    '''
    parser = argparse.ArgumentParser(description="Computes the color "
        "histogram of the specified image. See README.md for more "
        "information, and LICENSE for terms of use.")
    parser.add_argument("-d", action="store_true", help="display a pop-up "
        "window of the histogram information")
    parser.add_argument("filename", type=str, help="the name of the image "
        "file to process")
    return parser.parse_args()


def display_histogram(data, filename):
    '''
    Uses matplotlib to display histogram information.

    @param data the color histogram data
    @type data dict(red, green, blue)
    '''
    pyplot.plot(data[RED], color='r')
    pyplot.plot(data[GREEN], color='g')
    pyplot.plot(data[BLUE], color='b')
    pyplot.xlim([0, 256])
    pyplot.title("Color Histogram for {}".format(filename))
    pyplot.xlabel("Intensity (0 - 255)")
    pyplot.ylabel("Count")
    pyplot.grid(True)
    pyplot.show()


def weighted_means(data):
    '''
    Calcluates the weighted means for the histogram data.

    @param data the color histogram data
    @type data dict(red, green, blue)

    @return the weighted means for each component
    @rtype dict(red, green, blue)
    '''
    wred = 0
    wgreen = 0
    wblue = 0

    for i in xrange(256):
        wred += (data[RED][i] * i)
        wgreen += (data[GREEN][i] * i)
        wblue += (data[BLUE][i] * i)

    wred /= sum(data[RED])
    wgreen /= sum(data[GREEN])
    wblue /= sum(data[BLUE])

    return {RED: wred, BLUE: wblue, GREEN: wgreen}


def print_histogram(data):
    '''
    Prints out histogram data.

    @param data the color histogram data
    @type data dict(red, green, blue)
    '''
    print("Intensity |    Red     |    Green   |    Blue    |")
    print("----------+------------+------------+------------+")
    for i in xrange(256):
        print(" {:<8} | {:<10} | {:<10} | {:<10} |".format(
            i, data[RED][i], data[GREEN][i], data[BLUE][i]
        ))
    wmeans = weighted_means(data)
    print("----------+------------+------------+------------+")
    print("Wgt-Mean  | {:<10} | {:<10} | {:<10} |".format(
            wmeans[RED], wmeans[GREEN], wmeans[BLUE]
        ))


def compute_histogram(filename):
    '''
    Computes the histogram data for the specified file.

    @param filename the name of the file to open
    @type filename str

    @return the computed histogram data
    @rtype dict(red, green, blue)
    '''
    image = cv2.imread(filename)
    if image.ndim == 1:
        blue = cv2.calcHist([image], [0], None, [256], [0, 256])
        green = cv2.calcHist([image], [0], None, [256], [0, 256])
        red = cv2.calcHist([image], [0], None, [256], [0, 256])
    elif image.ndim == 3:
        blue = cv2.calcHist([image], [0], None, [256], [0, 256])
        green = cv2.calcHist([image], [1], None, [256], [0, 256])
        red = cv2.calcHist([image], [2], None, [256], [0, 256])
    else:
        logging.critical("Unknown color model for image!")
        sys.exit(1)

    data = {
        RED: squeeze(asarray(blue.astype(int))),
        GREEN: squeeze(asarray(green.astype(int))),
        BLUE: squeeze(asarray(red.astype(int)))
    }
    return data


def main(args):
    '''
    Runs the main program on the supplied arguments. Attempts to verify if
    the file name supplied is valid, and if so, will compute the histogram
    data for the file. Will optionally display an image of the histogram
    data.
    '''
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    if not os.path.isfile(args.filename):
        logging.critical("The file [{}] does not exist".format(args.filename))
        sys.exit(1)

    data = compute_histogram(args.filename)

    if args.d:
        display_histogram(data, args.filename)

    print_histogram(data)

###############################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
