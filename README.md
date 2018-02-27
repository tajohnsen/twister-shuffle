# twister-shuffle
A simple python script that generates commands for the game Twister by Hasbro.

Uses gTTS and pygame for playing audio.  To install use:<br />
Python 2:  pip install --upgrade gTTS pygame<br />
Python 3:  pip3 install --upgrade gTTS pygame

If pip fails, try upgrading it and try again.<br />
Python 2:  pip install --upgrade pip<br />
Python 3:  pip3 install --upgrade pip

If pygame fails specifically, try installing from apt/yum.<br />
apt install python-pygame python3-pygame<br />
yum install python-pygame python3-pygame

Simple Usage
------ -----
To get command line help:

```
$ python twister.py -h
usage: twister.py [-h] [-s seconds] [-n]

Give twister commands every 10 seconds.

optional arguments:
  -h, --help            show this help message and exit
  -w seconds, --wait seconds
                        number of seconds between each command
  -n, --no-audio        only display commands to screen
  -a, --animate         animate text version of spinning
  -c, --countdown       animate text version of spinning
  -l, --lift-up         add lift "up in the air" to wheel
  -s [filename], --spinners-choice [filename]
                        add spinners choice to wheel; import from filename
```

*Spinner's Choice* is where a player can choose a special rule for that spin.  This program allows the user to come up with a list of idea's and which will be played randomly.

Example
-------

```
$ python3 twister
right arm blue
right leg red
left arm red 
left leg yellow
right arm green
```
