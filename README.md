# twister-shuffle
A simple python script that generates commands for the game Twister by Hasbro.

Uses gTTS and pygame for playing audio.  To install use:
Python 2:  pip install --upgrade gTTS pygame
Python 3:  pip3 install --upgrade gTTS pygame

If pip fails, try upgrading it and try again.
Python 2:  pip install --upgrade pip
Python 3:  pip3 install --upgrade pip

If pygame fails specifically, try installing from apt/yum.
apt install python-pygame python3-pygame
yum install python-pygame python3-pygame

Simple Usage
------ -----
To get command line help:
$ python twister.py -h
usage: twister.py [-h] [-s seconds] [-n]

Give twister commands every 10 seconds.

optional arguments:
  -h, --help            show this help message and exit
  -s seconds, --wait seconds
                        number of seconds between each command
  -n, --no-audio        only display commands to screen
  
Example
-------
$ python3 twister
right arm blue
right leg red
left arm red 
left leg yellow
right arm green
