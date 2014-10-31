#!/usr/bin/env python
'''
Copyright (C) 2014 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

Simple application to split an image into the red, green and blue components.
'''
# I M P O R T S ###############################################################

import argparse, cv2, os, sys, logging

# C O N S T A N T S ###########################################################

RED = "red"
GREEN = "green"
BLUE = "blue"

# F U N C T I O N S ###########################################################

def parse_arguments():
    '''
    Parses the command line arguments passed to the program.

    @return a named tuple containing the parsed arguments
    '''
    parser = argparse.ArgumentParser(description="Splits the image into its "
        "red, green and blue channels. See README.md for more "
        "information, and LICENSE for terms of use.")
    parser.add_argument("filename", type=str, help="the name of the image "
        "file to process")
    return parser.parse_args()


def generate_new_filename(filename, prefix):
    '''
    Generates a new filename with a new prefix in front of the filename.

    @param filename: the name of the original file
    @type filename: str

    @param prefix: the prefix to add to the filename
    @type prefix: str

    @return: the new filename complete with path
    '''
    directory, name = os.path.split(filename)
    return os.path.join(directory, prefix + name)


def process_file(filename):
    '''
    Open the file, and separate the R, G, and B channels. Save each channel
    to a separate file.

    @param filename: the name of the file to process
    @type filename: str
    '''
    image = cv2.imread(filename)
    if image.ndim == 1:
        logging.critical("Image is grayscale")
        sys.exit(1)

    # Create the blue image
    image = cv2.imread(filename)
    image[:, :, 1] = 0
    image[:, :, 2] = 0
    newfile = generate_new_filename(filename, "b-")
    cv2.imwrite(newfile, image)

    # Create the green image
    image = cv2.imread(filename)
    image[:, :, 0] = 0
    image[:, :, 2] = 0
    newfile = generate_new_filename(filename, "g-")
    cv2.imwrite(newfile, image)

    # Create the red image
    image = cv2.imread(filename)
    image[:, :, 0] = 0
    image[:, :, 1] = 0
    newfile = generate_new_filename(filename, "r-")
    cv2.imwrite(newfile, image)


def main(args):
    '''
    Runs the main program on the supplied arguments. Attempts to verify if
    the file name supplied is valid, and if so, will split the image and save
    three new files with 'r-<imagename>', 'g-<imagename>', 'b-<imagename>'.
    '''
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO)

    if not os.path.isfile(args.filename):
        logging.critical("The file [{}] does not exist".format(args.filename))
        sys.exit(1)

    process_file(args.filename)


###############################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
