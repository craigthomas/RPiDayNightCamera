# Raspberry Pi - Day, Night NOIR Camera

## What is it?

This project represents a simple Python script that will take pictures
using a Raspberry PI camera module. The main difference between this 
script and the `raspistill` command is that it will turn the red LED
off before taking pictures, and can automatically detect when to 
switch between night and day mode settings.

The main purpose of this project is to assist with gathering image 
samples for my Machine Learning Deer Detector project (you can read
more about it [here](http://craigthomas.ca/blog/2014/08/04/deer-detection-with-machine-learning-part-1/)).

The project contains code to:

* Take a set number of pictures with the Raspberry Pi camera
* Compute the color histogram of an image
* Switch between user-specified day and night settings automatically

Adapted from the [PiCamera](http://picamera.readthedocs.org/en/latest/recipes1.html)
basic recipes.


## License

This project makes use of an MIT style license. Please see the file called 
LICENSE for more information. 


## Requirements

You will need a Raspberry Pi with a Pi Camera module installed. It is 
recommended that you install the latest version of [Raspbian](http://www.raspbian.org/) 
with the Pi Camera module enabled (do this using `sudo raspi-config`). 
Because the script requires direct access to the camera, you will
also need to run it as root with `sudo`.

In addition to the Raspberry Pi Camera, you will need the following
Python packages installed:

* numpy
* matplotlib
* opencv

This can generally be accomplished on the Raspberry Pi with:

    sudo apt-get install python-opencv python-matplotlib


## Running

### Command Line Help

There are several options available for the program. Running the script
with the `-h` option will display a helpful description of the options:

    python rpinoledcamera.py -h


### Taking Pictures

To take pictures of various objects, you can specify the number of pictures
to take as well as a time delay between successive pictures. For example,
to take 10 pictures:

    sudo python rpinoledcamera.py -n 10

To take 10 pictures with a delay of 5 seconds between each:

    sudo python rpinoledcamera.py -n 10 -d 5

Saving files to a different path:

    sudo python rpinoledcamera.py -p /path/to/save/to

Set night time conditions:

    sudo python rpinoledcamera.py -g

Take pictures until interrupted:

    sudo python rpinoledcamera.py -n 0


### Adjusting for light conditions

You can instruct the camera module to attempt to adjust for light conditions
by specifying the `--auto` switch:

    sudo python rpinoledcamera.py --auto -n 0

This will continue taking pictures until the program is interrupted. In order
to switch between day and night mode, you can specify at what light level
you want to make the swap on. For example, if the camera is in night mode,
then increasing light levels will make the picture brighter and brighter 
until the entire image is white. To swap to day mode, the camera calculates
the R, G, and B average intensities, and compares it to the `--day` value.
If the intensities are greater than the `--day` value, it will attempt to 
turn the camera on to day mode. The opposite occurs for `--night` values.

Both `--day` and `--night` are values in the range of 0 - 255. For example,
to get the camera to switch to day mode when the average pixel intensity 
reaches 240, and switch to night mode when the average pixel intensity reaches
30:

    sudo python rpinoledcamera.py --auto --day 240 --night 30 -n 0


### Calculating Histograms

To calcuate the histogram of an image, simply run the histogram 
program on the specified image. The intensity values will be
printed out on the standard out device:

    python histogram.py myimagefile.jpg

If you want to display the histogram data graphically, add the
`-d` option:

    python histogram.py myimagefile.jpg -d

The main camera application uses the histogram routines to figure out when
to swap between day and night modes.
