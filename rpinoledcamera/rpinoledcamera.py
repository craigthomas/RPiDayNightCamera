#!/usr/bin/env python
'''
Simple PyCamera application. Will take any number of pictures with the 
specified duration between snapshots in seconds. Optionally, will not turn on
the LED for the camera.
'''
# I M P O R T S ###############################################################

import RPi.GPIO as GPIO
import os, sys, argparse, logging

from time import strftime, localtime, sleep
from picamera import PiCamera

# C O N S T A N T S ###########################################################

CAMERA_LED = 5
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"

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
    return parser.parse_args()


def validate_path(path):
    '''
    Checks to see if the path is valid. Will return True on a valid path,
    False otherwise.
 
    @param path the path to validate
    @type path str
   
    @returns True if the path is valid, false otherwise
    '''
    return os.path.exists(path)
 

def take_snapshot(camera, path, ext):
    '''
    Takes a single picture, and stores it as a file in the specified path.
    
    @param camera the PiCamera to use to take pictures
    @type camera PiCamera
    
    @param path the validated path to store the file under
    @type path str
    '''
    filename = strftime(TIMESTAMP_FORMAT, localtime())
    camera.capture(os.path.join(path, "{}.{}".format(filename, ext)))


def main(args):
    '''
    Will loop and take snapshots from the camera after the specified number
    of seconds delay. 

    @param args the parsed command line arguments
    @type args named tuple
    '''
    logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(message)s',
        level = logging.INFO)

    if not validate_path(args.p):
        logging.critical("Path [{}] is not a directory".format(args.p))
        sys.exit(1)

    logging.info("Taking {} picture(s)".format(args.n))

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CAMERA_LED, GPIO.OUT, initial=False)
    camera = PiCamera()
    GPIO.output(CAMERA_LED, False)

    for snapshot_num in xrange(args.n):
        logging.info("Taking snapshot ({} of {})".format(snapshot_num + 1, 
            args.n))
        take_snapshot(camera, args.p, args.t)
        logging.info("Sleeping for {} second(s)".format(args.d))
        sleep(args.d)

    logging.info("Execution complete")
    

###############################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
