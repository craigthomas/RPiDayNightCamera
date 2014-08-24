#!/usr/bin/env python
'''
Copyright (C) 2014 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

Simple PyCamera application. Will take any number of pictures with the 
specified duration between snapshots in seconds. Optionally, will not turn on
the LED for the camera.
'''
# I M P O R T S ###############################################################

import os, sys, argparse, logging

from time import sleep
from picamera import PiCamera
from fractions import Fraction

# F U N C T I O N S ###########################################################

def parse_arguments():
    '''
    Parses the command line argments passed to the program.

    @returns a named tuple containing the parsed arguments
    '''
    parser = argparse.ArgumentParser(description = "Takes pictures with a "
        "Raspberry Pi camera. See README.md for more information, and LICENSE "
        "for terms of use.")
    parser.add_argument("-n", metavar = "NUMBER", help = "the number of "
        "pictures to take (default 1)", default = 1, type = int)
    parser.add_argument("-d", metavar = "DELAY", help = "delay in seconds "
        "between pictures (default 0)", default = 0, type = int)
    parser.add_argument("-p", metavar = "PATH", help = "location to store "
        "generated images", default = ".", type = str)
    parser.add_argument("-t", metavar = "TYPE", help = "filetype to store "
        "images as (default jpg)", default = "jpg", type = str)
    parser.add_argument("-g", action = "store_true", help = "adjust for "
        "night conditions")
    return parser.parse_args()

def main(args):
    '''
    Will loop and take snapshots from the camera after the specified number
    of seconds delay. 

    @param args the parsed command line arguments
    @type args named tuple
    '''
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
        level = logging.INFO)

    if not os.path.exists(args.p):
        logging.critical("Path [{}] is not a directory".format(args.p))
        sys.exit(1)

    cam = PiCamera()
    cam.led = False

    if args.g:
        cam.framerate = Fraction(1, 6)
        cam.shutter_speed = 6000000
        cam.exposure_mode = 'off'
        cam.ISO = 800
        cam.exposure_compensation = 25
        cam.awb_mode = 'off'
        cam.awb_gains = (2.0, 2.0)
        logging.info("Waiting for auto white balance")
        sleep(10)

    logging.info("Taking {} picture(s)".format(args.n))
    cam.start_preview()

    fullfilename = "{timestamp}." + args.t
    fullfilename = os.path.join(args.p, fullfilename)

    try:
        for i, filename in enumerate(cam.capture_continuous(fullfilename)):
            logging.info("Taking snapshot ({} of {})".format(i + 1, args.n))
            if not args.d == 0:
                logging.info("Sleeping for {} second(s)".format(args.d))
                sleep(args.d)
            if i + 1 == args.n:
                break
    finally:
        cam.stop_preview()

    logging.info("Execution complete")
    

###############################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
