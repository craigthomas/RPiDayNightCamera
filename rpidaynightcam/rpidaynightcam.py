#!/usr/bin/env python
"""
Copyright (C) 2014-2020 Craig Thomas
This project uses an MIT style license - see LICENSE for details.

Simple PyCamera application. Will take any number of pictures with the
specified duration between snapshots in seconds. Optionally, will not turn on
the LED for the camera.
"""
# I M P O R T S ###############################################################

import os, sys, argparse, logging

from time import sleep
from picamera import PiCamera
from fractions import Fraction
from histogram import compute_histogram, weighted_means

# G L O B A L S ###############################################################

DAY_MODE = "day"
NIGHT_MODE = "night"

# F U N C T I O N S ###########################################################


def parse_arguments():
    """
    Parses the command line argments passed to the program.

    :return: a named tuple containing the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Takes pictures with a "
        "Raspberry Pi camera. See README.md for more information, and LICENSE "
        "for terms of use."
    )
    parser.add_argument(
        "-n", metavar="NUMBER", help="the number of "
        "pictures to take (default 1, 0 = continuous)", default=1, type=int
    )
    parser.add_argument(
        "-d", metavar="DELAY", help="delay in seconds "
        "between pictures (default 0)", default=0, type=int
    )
    parser.add_argument(
        "-p", metavar="PATH", help="location to store "
        "generated images", default=".", type=str
    )
    parser.add_argument(
        "-t", metavar="TYPE", help="filetype to store "
        "images as (default jpg)", default="jpg", type=str
    )
    parser.add_argument(
        "-g", action="store_true", help="adjust for "
        "night conditions"
    )
    parser.add_argument(
        "--night", help="the intensity value at "
        "which to switch to night-time image settings (default 40, "
        "requires --auto)", default=40, type=int
    )
    parser.add_argument(
        "--day", help="the intensity value at "
        "which to switch to day-time image settings (default 230, "
        "requires --auto)", default=230, type=int
    )
    parser.add_argument(
        "--auto", help="automatically switch between "
        "day-time and night-time image settings", action="store_true"
    )
    parser.add_argument(
        "--check", help="check for day or night time "
        "settings after this many snapshots (default 5, requires "
        "--auto)", default=5, type=int
    )
    return parser.parse_args()


def night_mode(cam):
    """
    Switches the camera to night mode.

    :param cam: the PiCamera to tweak
    """
    logging.info("Switching to night-time mode")
    cam.framerate = Fraction(1, 6)
    cam.shutter_speed = 3000000
    cam.exposure_mode = 'off'
    cam.ISO = 800
    cam.exposure_compensation = 25
    cam.awb_mode = 'off'
    cam.awb_gains = (2.0, 2.0)
    logging.info("Waiting for auto white balance")
    sleep(10)


def day_mode(cam):
    """
    Switches the camera to day mode.

    :@param cam: the PiCamera to tweak
    """
    logging.info("Switching to day-time mode")
    cam.shutter_speed = 0
    cam.exposure_mode = 'auto'
    cam.ISO = 200
    cam.exposure_compensation = 25
    cam.awb_mode = 'auto'
    logging.info("Waiting for auto white balance")
    sleep(10)


def main(args):
    """
    Will loop and take snapshots from the camera after the specified number
    of seconds delay.

    :param args: the parsed command line arguments
    """
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    if not os.path.exists(args.p):
        logging.critical("Path [{}] is not a directory".format(args.p))
        sys.exit(1)

    cam = PiCamera()
    cam.led = False
    mode = DAY_MODE

    if args.g:
        night_mode(cam)
        mode = NIGHT_MODE

    if args.n == 0:
        logging.info("Taking pictures")
    else:
        logging.info("Taking {} picture(s)".format(args.n))

    fullfilename = "{timestamp}." + args.t
    fullfilename = os.path.join(args.p, fullfilename)
    snapcounter = 1

    for i, filename in enumerate(cam.capture_continuous(fullfilename)):
        if args.n == 0:
            logging.info("Taking snapshot ({} mode)".format(mode))
        else:
            logging.info("Taking snapshot ({} of {}, {} mode)".format(
                   i + 1, args.n, mode))

        if args.auto and snapcounter > args.check:
            snapcounter = 0
            logging.info("Checking for day or night conditions")
            hist = compute_histogram(filename)
            means = weighted_means(hist)
            if means["red"] >= args.day and \
                    means["green"] >= args.day and \
                    means["blue"] >= args.day:
                day_mode(cam)
                mode = DAY_MODE

            if means["red"] <= args.night and \
                    means["green"] <= args.night and \
                    means["blue"] <= args.night:
                night_mode(cam)
                mode = NIGHT_MODE

        if args.auto:
            snapcounter += 1

        if not args.d == 0:
            delay = args.d

            # Adjust the delay for the night time frame speed
            if mode == NIGHT_MODE:
                delay -= 3

            logging.info("Sleeping for {} second(s)".format(delay))
            sleep(delay)

        if args.n > 0 and i + 1 == args.n:
            break

    logging.info("Execution complete")


###############################################################################

if __name__ == "__main__":
    main(parse_arguments())

# E N D   O F   F I L E #######################################################
