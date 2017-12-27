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

import random, time, argparse, sys
import tempfile
from pygame import mixer

LIMBS = ["arm", "leg"]
SIDES = ["right", "left"]
COLORS= ["red", "blue", "yellow", "green"]
WAIT = 10
AUDIO= True

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
        a.save(f.name)
        mixer.init()
        mixer.music.load(f.name)
        mixer.music.play()
        while mixer.music.get_busy(): # pause this script until the 
            time.sleep(.1)              # audio finishes

def pause(total=10):
    from sys import stdout
    start = time.time()
    while time.time() - start < total:
        move = get_move()
        stdout.write(move)
        stdout.flush()
        time.sleep(.05)
        stdout.write('\r')
        stdout.write(' '*len(move))
        stdout.write('\r')
        stdout.flush()

def main():
    while True:
        try:
            move = get_move()
            print(move)
            if AUDIO:
                play_move(move)
            pause(total=WAIT)
        except KeyboardInterrupt:
            exit(0)
    return 0

def parse_args():
    parser = argparse.ArgumentParser(
            description='Give twister commands every 10 seconds.')
    parser.add_argument('-s', '--wait', metavar='seconds', type=int,
            help='number of seconds between each command')
    parser.add_argument('-n', '--no-audio', action='store_true', 
            help='only display commands to screen')
    args = parser.parse_args()
    if args.wait:
        global WAIT
        WAIT = args.wait
    if args.no_audio:
        global AUDIO
        AUDIO=False

if __name__ == '__main__':
    args = parse_args()
    if AUDIO:
        try:
            import gtts
        except ImportError:
            AUDIO = False
            print("Cannot import audio utility.  Continuing without audio.")
            print("To install, try: pip{} install --upgrade gTTS".format( \
            '3' if sys.version_info > (3,0) else '2'))
    main()

