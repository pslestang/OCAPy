#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 Pierre-Samuel Le Stang (ps@lestang.fr)
#  
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

COLORS = False
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = 0
    pass

def color(enable=False):
    global COLORS
    if COLORS == 0:
        return False
    COLORS = enable
    return COLORS

class UserInput(object):
    """"""
    def __init__(self, question=None, choices=None, default=None):
        self.question = question
        self.choices = choices or []
        self.default = default

    def process(self):
        if not self.question or self.question == '':
            raise OCAPyInputException("Missing question for user, review your"
                                      " code...")
        choice_string=''
        for choice in self.choices:
            if choice_string != '':
                choice_string += '/'

            if choice == self.default:
                if COLORS:
                    choice = '%s%s*%s' % (Fore.GREEN, choice,
                                         Fore.WHITE)
                else:
                    choice = '%s*' % str(choice)


            choice_string += choice

        if choice_string != '':
            choice_string = '[%s]' % choice_string

        if COLORS:
            question = '%s%s%s %s: ' % (Style.BRIGHT, self.question, Style.NORMAL, choice_string)
        else:
            question = '%s %s: ' % (self.question, choice_string)

        value = raw_input('%s' % question)

        while (len(self.choices) and value not in self.choices):
            if value == '':
                value = self.default

            if len(self.choices) and value not in self.choices:
                if COLORS:
                    print "%s>>>>> Answer (%s%s%s) is not valid, allowed values: %s" % (Fore.RED, Style.BRIGHT, value, Style.NORMAL, self.choices)
                else:
                    print ">>>>> Answer (%s) is not valid, allowed values: %s" % (value, self.choices)

                value = raw_input('%s' % question)

        return value

if __name__ == '__main__':
    print UserInput(question='You know what?', choices=[ 'Yes', 'No', 'I\'m happy'],
                    default='Yes').process()
