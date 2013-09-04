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

import os
import stat
import sys
import codecs
import string
import random

from ConfigParser import SafeConfigParser
from OCAPy import OCAPy

class Config(object):
    """"""

    def __init__(self):
        self.file = '%s/.ocapyrc' % os.path.expanduser('~')
        self.profiles = []
        self.ocapy = None
        self.parser = None
        self.load()

    def add_profile(self, **kwargs):
        profile = Profile(parser=self.parser, **kwargs)
        self.profiles.append(profile)

    def set_default(self, profile=None):
        self.ocapy.default_profile = profile.name

    def load(self):
        parser = SafeConfigParser()

        if not os.path.exists(self.file):
            with open(self.file, 'a') as f:
                f.write('')

        with codecs.open(self.file, 'r', encoding='utf-8') as f:
            parser.read(f)

        self.parser = parser
        for section in parser.sections():
            options = parser.options(section)
            params = {}
            for option in options:
                params[option] = parser.get(section, option)

            if section == 'ocapy':
                self.ocapy = OcapyConfig(parser=self.parser, **params)
            elif str(section).startswith('profile-'):
                self.add_profile(parser=self.parser, **params)

    def save(self):
        if self.ocapy is None:
            default_profile = None
            if len(self.profiles) > 0:
                default_profile = self.profiles[0].name

            self.parser.add_section('ocapy')
            self.ocapy = OcapyConfig(default_profile=default_profile,
                                     base_url='https://api.ovh.com/1.0/',
                                     parser=self.parser)

        if self.ocapy.default_profile is None:
             if len(self.profiles) > 0:
                 self.set_default(profile=self.profiles[0])

        self.ocapy.save()

        for profile in self.profiles:
            profile.save()

        with open(self.file, 'w') as f:
            self.parser.write(f)

        if sys.platform.startswith('linux'):
            os.chmod(self.file, stat.S_IRUSR | stat.S_IWUSR)

class OcapyConfig(object):
    """Config parameters for Ocapy"""

    def __init__(self, default_profile=None, base_url=None, parser=None):
        self.section = 'ocapy'
        self.default_profile = default_profile
        self.base_url = base_url
        self.parser = parser

    def save(self):
        self.parser.set(self.section, 'default_profile',
                        str(self.default_profile))

class Profile(object):
    """modelises an authentication profile"""

    def __init__(self, name=None, app_key=None, app_secret=None,
                 consumer_key=None, base_url=None, parser=None):
        self.name = name
        self.app_key = app_key
        self.app_secret = app_secret
        self.consumer_key = consumer_key
        self.base_url = base_url
        self.parser = parser

        if self.name is None:
            self.name = ''.join(random.choice(string.ascii_uppercase +
                                              string.digits) for x in range(6))
        self.section = 'profile-%s' % self.name

        if not self.parser.has_section(self.section):
            self.parser.add_section(self.section)


    def save(self):
        if self.is_valid():
            self.parser.set(self.section, 'name', self.name)
            self.parser.set(self.section, 'app_key', self.app_key)
            self.parser.set(self.section, 'app_secret', self.app_secret)
            self.parser.set(self.section, 'consumer_key', self.consumer_key)
            self.parser.set(self.section, 'base_url', self.base_url)
        else:
            # TODO: warning or exception?
            pass

    def is_valid(self):
        ocapy = OCAPy(base_url=self.base_url, app_key=self.app_key,
                      app_secret=self.app_secret,
                      consumer_key=self.consumer_key)

        try:
            ocapy.me.get()
        except Exception:
            return False

        return True

if __name__ == '__main__':

    # Load config file $HOME/.ocapyrc
    config = Config()
    # Add a profile without name
    config.add_profile(base_url='https://api.ovh.com/1.0/',
                       app_key='appkey1',
                       app_secret='appsecret1',
                       consumer_key='consumerkey1',
                      )
    # Add an other one
    config.add_profile(base_url='https://api.ovh.com/1.0/',
                       app_key='appkey2',
                       app_secret='appsecret2',
                       consumer_key='consumerkey2',
                       name='name2'
                      )
    # Save the data
    # Default profile is the first profile added (unless ther is already one set)
    config.save()
