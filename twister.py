#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  twister.py
#
#  Copyright 2017  <tjohnsen@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import random, time, argparse, sys, os
import tempfile
from sys import stdout

LIMBS   = ["arm", "leg"]
SIDES   = ["right", "left"]
COLORS  = ["red", "blue", "yellow", "green"]
WAIT    = 10
AUDIO   = True
ANIMATE = False
WIN     = 'nt' in os.name
LAST    = None

def _rand(data):
    index = random.randint(0,len(data)-1)
    return data[index]

def get_move():
    limb = _rand(LIMBS)
    side = _rand(SIDES)
    color= _rand(COLORS)

    return ' '.join([side,limb,color])

def play_move(str_move):
    with tempfile.NamedTemporaryFile(mode='w') as f:
        a=gtts.gTTS(text=str_move, lang='en', slow=False)
        if WIN:
            f.delete=False
            f.close()
        a.save(f.name)
        mixer.init()
        mixer.music.load(f.name)
        mixer.music.play()
        try:
            while mixer.music.get_busy(): # pause this script until the
                time.sleep(.1)              # audio finishes
        except KeyboardInterrupt:
            if WIN: # if windows we need to delete the current file
                mixer.quit() # quit to make file available to delete
                os.remove(f.name)
            raise
        if WIN:
            global LAST
            if LAST is not None:
                os.remove(LAST)
            LAST = f.name

def animate(delay=10):
    delay_width = len(str(delay))
    increment = .1/delay
    rest = increment
    sides,limbs,colors=len(SIDES),len(LIMBS),len(COLORS)
    side = random.randint(0,sides-1)
    limb = random.randint(0,limbs-1)
    color = random.randint(0,colors-1)
    start = time.time()
    x,y,z,=limb,side,color
    duration = time.time() - start
    while duration < delay:
        z+=1
        z%=colors
        if z == color:
            y+=1
            y%=sides
            if y == side:
                x+=1
                x%=limbs
        time_left = "[{delay:{width}d}] ".format(\
            delay=int(delay-duration)+1, width=delay_width)
        move = ' '.join([SIDES[y],LIMBS[x],COLORS[z]])
        flash_move(time_left + move,rest)
        rest+=increment
        duration = time.time() - start
    return move


def pause(delay=10):
    delay_width = len(str(delay))
    start = time.time()
    duration = time.time() - start
    while duration < delay:
        move = get_move()
        time_left = "[{delay:{width}d}] ".format(\
            delay=int(delay-duration)+1, width=delay_width)
        flash_move(time_left + move)
        duration = time.time() - start

def flash_move(move, rest=.05):
    stdout.write(move)
    stdout.flush()
    time.sleep(rest)
    stdout.write('\r')
    stdout.write(' '*len(move))
    stdout.write('\r')

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("{} is invalid (must be positive)".format(value))
    return ivalue

def parse_args():
    parser = argparse.ArgumentParser(
            description='Give twister commands every 10 seconds.')
    parser.add_argument('-s', '--wait', metavar='seconds', type=positive_int,
            help='number of seconds between each command')
    parser.add_argument('-n', '--no-audio', action='store_true',
            help='only display commands to screen')
    parser.add_argument('-a', '--animate', action='store_true',
            help='animate text version of spinning')
    args = parser.parse_args()
    if args.wait:
        global WAIT
        WAIT = args.wait
    if args.no_audio:
        global AUDIO
        AUDIO=False
    if args.animate:
        global ANIMATE
        ANIMATE=True

def main():
    while True:
        try:
            if ANIMATE:
                move = animate(WAIT)
            else:
                move = get_move()
            highlighted = "-= [{}] =-".format(move.upper())
            stdout.write(highlighted)
            stdout.flush()
            if AUDIO:
                play_move(move)
            stdout.write('\r{}\r'.format(' '*len(highlighted)))
            print(move.upper())
            if not ANIMATE:
                pause(delay=WAIT)
        except KeyboardInterrupt:
            if WIN and LAST is not None:
                mixer.quit()
                os.remove(LAST)
            stdout.write('\n')
            exit(0)
    return 0

if __name__ == '__main__':
    args = parse_args()
    if AUDIO:
        try:
            import gtts
            from pygame import mixer
        except ImportError:
            AUDIO = False
            print("Cannot import audio utility.  Continuing without audio.")
            print("To install, try: pip{} install --upgrade gTTS pygame".format( \
            '3' if sys.version_info > (3,0) else '2'))
    main()
