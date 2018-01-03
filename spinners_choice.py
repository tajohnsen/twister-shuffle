#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  spinners_choice.py
#
#  Copyright 2017 Tim <tjohnsen@gmail.com>
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
import random

class Choice():
    def __init__(self):
        self.commands = []
        self.len = 0    # initialize with 0 elements

    def load(self, filename):
        """Load commands from file."""
        try:
            with open(filename,'r') as f:
                for line in f.readlines():
                    line=line.strip()
                    if len(line) == 0:
                        continue # don't include this line if it's blank
                    if '#' in line: # allow comments, removing them
                        line = line.split('#',1)[0]
                    if '{}' not in line:
                        if line.lower()[0:4] != "and ": # if it doesn't start with and, add 'and'
                            line = 'and ' + line.strip()
                    self.commands.append(line)
        except:
            print("Cannot open {}!".format(filename))
        self.len = len(self.commands)

    def get_random_str(self):
        size = len(self.commands)
        if size == 0:
            return None # list is empty
        return self.commands[random.randint(0,size-1)]

    def get(self, index):
        """Return string at index.
        If the index is not an int within the list it returns None."""
        if type(index) is not int or index >= len(self.commands):
            return None
        return self.commands[index]

    def get_move_str(self,move):
        """Return a given Twister move with a random choice.
        Without a custom file it will return move, ' and spinners choice'
        If a {} is NOT in the custom line, return move, choice
        If a {} IS in the custom line, return move.formated, None"""
        if len(self.commands) == 0:
            return move, ', and spinner\'s choice'  # return as is, we can't do anything here
        choice = self.get_random_str()
        if '{}' not in choice:
            return move.strip(), choice.strip()
        else:
            return choice.format(move), None
