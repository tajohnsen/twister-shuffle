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

from spinners_choice import Choice
import random
import time
import argparse
import sys
import os
import atexit
import tempfile
from sys import stdout

LIMBS = ["hand", "foot"]
SIDES = ["right", "left"]
COLORS = ["red", "blue", "yellow", "green"]
_COLORS = COLORS[:]  # copy to maintain original colors (if user adds to wheel)
WAIT = 10
AUDIO = True
ANIMATE = False
COUNT = False
CHOICE = False
WIN = 'nt' in os.name
LAST = None
ROUNDS = 0  # count how many rounds the game lasted


def _rand(list_data):
    """Return a random element from a given list.
    Will return None if the argument is not a list."""
    if type(list_data) is not list:
        return None
    index = random.randint(0, len(list_data) - 1)
    return list_data[index]


def get_move():
    """Return a randomly generated Twister move."""
    limb = _rand(LIMBS)
    side = _rand(SIDES)
    color = _rand(COLORS)

    return ' '.join([side, limb, color])


def play_file(file_name):
    """Use pygame...music.play to play file_name"""
    from pygame import mixer, error  # done again in case used as library
    try:
        mixer.init()
        mixer.music.load(file_name)
        mixer.music.play()
        while mixer.music.get_busy():  # pause this script until the
            time.sleep(.01)  # audio finishes
    except KeyboardInterrupt:
        mixer.quit()  # quit to make file available to delete
        raise  # re-raise for caller to handle rest of delete (possibly)
    except error:  # pygame.error
        print("Error loading {}! File has been removed!".format(file_name))
        os.remove(file_name)


def play_move(str_move):
    """Taking an input str_move, save the text to speech, save it to a
    temporary file, and play the audio."""
    with tempfile.NamedTemporaryFile(mode='w') as f:
        if WIN:
            global LAST
            if LAST is None:
                LAST = [f.name]
            else:
                LAST.append(f.name)
            f.delete = False
            f.close()
        try:  # we must catch here because of Windows (to delete file)
            save_sound_file(str_move, f.name)
            play_file(f.name)
        except KeyboardInterrupt:
            if WIN:  # if windows we need to delete the current file
                os.remove(f.name)
            raise
        if WIN and len(LAST) == 2:
            os.remove(LAST[0])
            LAST.remove(LAST[0])


def play_move_stored(str_move, download=True):
    file_name = "audio/{}.mp3".format(str_move.replace(' ', '_'))
    if os.path.exists(file_name):
        try:
            # ~ print("playing stored file: {}".format(file_name))
            play_file(file_name)
        except KeyboardInterrupt:
            raise  # just reraise since we aren't deleting here
    elif download:
        # ~ print("downloading file")
        # if file isn't there download it
        if not os.path.isdir('audio'):
            os.mkdir('audio')
        save_sound_file(str_move, 'audio/{}.mp3'.format(str_move.replace(' ', '_')))
        play_move_stored(str_move, download=False)  # recursive call but don't reattempt download
    else:
        # ~ print("not saving downloaded mp3")
        play_move(str_move)  # if download isn't set, use tempfile


def save_sound_file(text, destination):
    """Save text string as an MP3 to destination."""
    import gtts
    try:
        tts = gtts.gTTS(text=text, lang='en', slow=False)
        tts.save(destination)
    except KeyboardInterrupt:
        # if the download was interrupted erase it because it's probably bad
        if os.path.exists(destination):
            os.remove(destination)
            raise


def download_moves():
    """Download all mp3 files for basic moves."""
    download_message = "Performing initial download..."
    sys.stdout.write(download_message)
    sys.stdout.flush()
    current = 0
    total = len(SIDES) * len(LIMBS) * len(COLORS)
    total += 0 if not CHOICE else CHOICES.len
    display = "{}%"
    display_last = display.format(int((current * 100) / total))
    sys.stdout.write(display_last);
    sys.stdout.flush()
    if not os.path.isdir('audio') and not os.path.exists('audio'):
        os.mkdir('audio')
    for side in SIDES:
        for limb in LIMBS:
            for color in COLORS:
                if 'spinners choice' == color:
                    for _color in _COLORS:
                        str_move = ' '.join([side, limb, _color, 'and', color])
                        file_name = 'audio/{}.mp3'.format(str_move.replace(' ', '_'))
                        if not os.path.exists(file_name):
                            save_sound_file(str_move, file_name)
                else:
                    str_move = ' '.join([side, limb, color])
                    file_name = 'audio/{}.mp3'.format(str_move.replace(' ', '_'))
                    if not os.path.exists(file_name):
                        save_sound_file(str_move, file_name)
                current += 1
                sys.stdout.write('\b' * len(display_last))  # backspace over last display
                display_last = display.format(int((current * 100) / total))
                sys.stdout.write(display_last)
                sys.stdout.flush()
    if CHOICE:
        for index in range(CHOICES.len):
            str_move = CHOICES.get(index)
            if '{}' not in str_move:  # skip downloading formatted types
                file_name = 'audio/{}.mp3'.format(str_move.replace(' ', '_'))
                if not os.path.exists(file_name):
                    save_sound_file(str_move, file_name)
            current += 1
            sys.stdout.write('\b' * len(display_last))  # backspace over last display
            display_last = display.format(int((current * 100) / total))
            sys.stdout.write(display_last)
            sys.stdout.flush()

    sys.stdout.write('\r')
    sys.stdout.write(' ' * (len(download_message) + len(display_last)))
    sys.stdout.write('\r')


def time_left_str(delay, duration):
    """Return a formatted string of seconds left."""
    time_left = ''
    if COUNT:
        time_left += "[{delay:{width}d}] ".format( \
            delay=int(delay - duration) + 1, width=len(str(delay)))
    return time_left


def animate(delay=10):
    """Display twister commands in order, emulating spinning a spinner."""
    increment = .25 / delay
    rest = increment
    sides, limbs, colors = len(SIDES), len(LIMBS), len(COLORS)
    side = random.randint(0, sides - 1)
    limb = random.randint(0, limbs - 1)
    color = random.randint(0, colors - 1)
    start = time.time()
    x, y, z, = limb, side, color
    duration = time.time() - start
    while duration < delay:
        z += 1
        z %= colors
        if z == color:
            y += 1
            y %= sides
            if y == side:
                x += 1
                x %= limbs
        time_left = time_left_str(delay, duration)
        move = ' '.join([SIDES[y], LIMBS[x], COLORS[z]])
        flash_move(time_left + move, rest)
        duration = time.time() - start
        if duration > delay / 2.0:  # go quick for the first half
            rest += increment
    return move


def pause(delay=10):
    """Delay number of seconds passed in.  During the pause, display
    other random moves to the screen for entertainment purposes."""
    start = time.time()
    duration = 0
    while duration < delay:
        move = get_move()
        time_left = time_left_str(delay, duration)
        flash_move(time_left + move)
        duration = time.time() - start


def flash_move(move, rest=.05):
    """Display a string passed in as an argument, rest for a certain
    amount of time passed in as the rest argument, overwrite that
    text with spaces (to erase) and then return.

    Note:  Display buffer is not flushed after erasing message."""
    stdout.write(move)
    stdout.flush()
    time.sleep(rest)
    stdout.write('\r')
    stdout.write(' ' * len(move))
    stdout.write('\r')


def positive_int(value):
    """Ensure argument is a positive integer."""
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("{} is invalid (must be positive)".format(value))
    return ivalue


def init_choice(filename=None):
    """If using spinner's choices, """
    global CHOICES
    CHOICES = Choice()
    if filename is not None:
        CHOICES.load(filename)
    global COLORS
    COLORS.append('spinners choice')
    # ~ COLORS = ['spinners choice']


def move_choice(move):
    """Take a move that contains spinners choice and
    return a spinners choice string."""
    if 'spinners choice' in move:
        move = move[0:move.find('spinners choice')]  # cut off choice
        move += _rand(_COLORS)  # append random color
    return CHOICES.get_move_str(move)


def test_choices():
    for choice in CHOICES.commands:
        print(choice)
        move = get_move()
        # don't use move_choice to avoid random choice
        if 'spinners choice' in move:
            move = move[0:move.find('spinners choice')]  # cut off choice
            move += _rand(_COLORS)  # append random color
        if '{}' in choice:
            move = choice.format(move)
        else:
            move = ' '.join([move, choice])
        print(move)
        play_move(move)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Give twister commands every 10 seconds.')
    # parser.add_argument('--clean', action='store_true',
    #        help='erase downloaded files and exit')
    parser.add_argument('-w', '--wait', metavar='seconds', type=positive_int,
                        help='number of seconds between each command')
    parser.add_argument('-n', '--no-audio', action='store_true',
                        help='only display commands to screen')
    parser.add_argument('-a', '--animate', action='store_true',
                        help='animate text version of spinning')
    parser.add_argument('-c', '--countdown', action='store_true',
                        help='animate text version of spinning')
    parser.add_argument('-l', '--lift-up', action='store_true',
                        help='add lift "up in the air" to wheel')
    parser.add_argument('-d', '--no-download', action='store_true',
                        help="don't perform the initial download of audio files")
    parser.add_argument('-s', '--spinners-choice', action='store',
                        help='add spinners choice to wheel; import from filename',
                        const='', nargs="?", metavar='filename')
    args = parser.parse_args()
    # if args.clean:
    #    pass
    #    exit(0)
    if args.wait:
        global WAIT
        WAIT = args.wait
    if args.spinners_choice is not None:
        global CHOICE
        CHOICE = True
        chfile = None \
            if args.spinners_choice == '' \
            else args.spinners_choice
        init_choice(filename=chfile)
    if args.lift_up:
        global COLORS
        COLORS.append("up in the air")

    # ~ from pprint import pprint
    # ~ pprint(args)
    # ~ exit(0)
    global AUDIO
    AUDIO = not args.no_audio
    global COUNT
    COUNT = args.countdown
    global ANIMATE
    ANIMATE = args.animate
    return args


def at_exit():
    if WIN and LAST is not None:
        mixer.quit()
        for rem_file in LAST:
            try:
                os.remove(rem_file)
            except:
                continue  # if remove fails move on to next`


def main():
    global ROUNDS
    while True:
        try:
            if ANIMATE:
                move = animate(WAIT)
            else:
                move = get_move()
            SC = 'spinners choice' in move.lower()
            if SC:
                move, choice = move_choice(move)
                if choice is None:
                    SC = False  # treat as regular if formatted
                else:
                    move_combined = ' '.join([move, choice])
            if not SC:  # not else to pick up on change above
                move_combined = move
            highlighted = "-= [{}] =-".format(move_combined.upper())
            stdout.write(highlighted)
            stdout.flush()
            ROUNDS += 1  # move selected, this round counts
            if AUDIO:
                play_move_stored(move)
                if SC:
                    play_move_stored(choice)
            stdout.write('\r{}\r'.format(' ' * len(highlighted)))
            print(move_combined.upper())
            if 'spinner\'s choice' in move_combined.lower():
                pause()  # delay 10 seconds since someone has to think
            if not ANIMATE:
                pause(delay=WAIT)
        except KeyboardInterrupt:
            if WIN and LAST is not None:
                mixer.quit()
                os.remove(LAST)
            print("\nGame lasted {} rounds!".format(ROUNDS))
            exit(0)
    return 0


if __name__ == '__main__':
    parsed_args = parse_args()
    if AUDIO:
        try:
            import gtts
            from pygame import mixer

            atexit.register(at_exit)
            if not parsed_args.no_download:  # if user didn't skip download
                download_moves()
            # ~ test_choices()
            # ~ exit(0)
        except KeyboardInterrupt:
            # can interrupt the download of audio files
            # exit with error
            print("\nInterrupted download of audio files.")
            print("If there is a problem with the download use --no-audio to not use the audio feature.")
            print("Use --no-download to skip the initial download. (will download per first use)")
            exit(1)
        except ImportError:
            AUDIO = False
            print("Cannot import audio utility.  Continuing without audio.")
            print("To install, try: pip{} install --upgrade gTTS pygame".format(
                '3' if sys.version_info > (3, 0) else '2'))
    main()
