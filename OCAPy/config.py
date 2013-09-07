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

"""
.. module:: config
    :platform: Unix
    :synopsis: This module defines classes for OCAPy configuration

.. moduleauthor:: Pierre-Samuel Le Stang <ps@lestang.fr>


"""

import os
import stat
import sys
import codecs
import string
import random
import logging

from ConfigParser import SafeConfigParser

class Config(object):
    """Defines the main config class
    
    .. note::

       The configuration file is stored in the user's home directory and is called .ocapyrc

    """

    def __init__(self):
        """is called when :class:`Config` is instantiated

    .. note::

        Current user's configuration is loaded as soon as :class:`OCAPy.Config` is instantiated

        """
        self.file = '%s/.ocapyrc' % os.path.expanduser('~')
        self.profiles = []
        self.ocapy = None
        self.parser = None
        self.load()

    def add_profile(self, name=None, app_key=None, app_secret=None, section=None,
                    consumer_key=None, base_url=None):
        """create a Profile instance and add it to profiles list attribute
        
        Keyword arguments:
        :param kwargs: keywords passed to :class:`Profile` for instantiation
        :return: the added :class:`Profile` instance

        """
        profile = Profile(parser=self.parser, name=name, app_key=app_key,
                          app_secret=app_secret, consumer_key=consumer_key,
                          base_url=base_url, section=section)
        self.profiles.append(profile)
        return profile

    def delete_profile(self, name):
        profile = self.profile(name)
        if profile is not None:
            profile.delete()

    def profile(self, name):
        profile = None
        for profile in self.profiles:
            if profile.name == name:
                break
            else:
                profile = None

        return profile

    def set_default(self, profile=None):
        """set default profile name to main ocapy configuration
        
        :param profile: a Profile instance

        """
        self.ocapy.profile = profile.name

    def load(self):
        self.parser = SafeConfigParser()

        if not os.path.exists(self.file):
            with open(self.file, 'a') as f:
                f.write('')

        self.parser.read(self.file)

        for section in self.parser.sections():
            options = self.parser.options(section)
            params = {}
            for option in options:
                params[option] = self.parser.get(section, option)
            params['section'] = section

            if section == 'ocapy':
                self.ocapy = OcapyConfig(parser=self.parser, **params)
            elif str(section).startswith('profile-'):
                self.add_profile(**params)

        if self.ocapy is None:
            self.ocapy = OcapyConfig(parser=self.parser,
                                     base_url='https://api.ovh.com/1.0/')

    def save(self):
        if self.ocapy.profile == '':
            if len(self.profiles) > 0:
                self.ocapy.profile = self.profiles[0].name
        self.ocapy.save()

        for profile in self.profiles:
            profile.save()

        with open(self.file, 'w') as f:
            self.parser.write(f)

        if sys.platform.startswith('linux'):
            os.chmod(self.file, stat.S_IRUSR | stat.S_IWUSR)

class OcapyConfig(object):
    """Config parameters for Ocapy"""

    def __init__(self, profile=None, base_url=None, section=None, parser=None):
        self.section = section or 'ocapy'
        self.profile = profile or ''
        self.base_url = base_url
        self.parser = parser

        if not self.parser.has_section(self.section):
            self.parser.add_section(self.section)

    def save(self):
        self.parser.set(self.section, 'base_url', self.base_url)
        self.parser.set(self.section, 'profile', str(self.profile))

class Profile(object):
    """modelises an authentication profile"""

    def __init__(self, name=None, app_key=None, app_secret=None,
                 consumer_key=None, base_url=None, section=None, parser=None):
        self.name = name
        self.app_key = app_key
        self.app_secret = app_secret
        self.consumer_key = consumer_key
        self.base_url = base_url
        self.parser = parser
        self.section = section

        if not self.parser.has_section(self.section) and self.section is not None:
            self.parser.add_section(self.section)


    def save(self):
        if self.name is None or self.name == '':
            if self.section is not None:
                self.parser.remove_section(self.section)
            self.name = ''.join(random.choice(string.ascii_uppercase + 
                                              string.digits) for x in range(6))
            self.section = 'profile-%s' % self.name
            self.parser.add_section(self.section)
    
        if self.section is None:
            self.section = 'profile-%s' % self.name
            self.parser.add_section(self.section)

        if self.is_valid():
            if self.parser.has_section(self.section):
                self.parser.set(self.section, 'name', self.name)
                self.parser.set(self.section, 'app_key', self.app_key)
                self.parser.set(self.section, 'app_secret', self.app_secret)
                self.parser.set(self.section, 'consumer_key', self.consumer_key)
                self.parser.set(self.section, 'base_url', self.base_url)
        else:
            logging.warning('Profile not valid, removing ....')
            self.delete()

    def delete(self):
        self.parser.remove_section(self.section)

    def is_valid(self):
        from OCAPy import OCAPy
        ocapy = OCAPy(base_url=self.base_url, app_key=self.app_key,
                      app_secret=self.app_secret,
                      consumer_key=self.consumer_key)

        try:
            ocapy.me.get()
        except Exception as e:
            logging.error('Profile validation error: %s' % e)
            return False

        return True

    def __str__(self):
        name = 'Name'
        base_url = 'Base URL'
        app_key = 'Application key'
        app_secret = 'Application secret'
        consumer_key = 'Consumer key'

        maxsize = 0
        for size in [len(name), len(base_url), len(app_key),
                     len(app_secret), len(consumer_key)]:
            if size > maxsize:
                maxsize = size

        output = '%s: %s' % (string.rjust(name, maxsize), self.name)
        output += '\n%s: %s' % (string.rjust(base_url, maxsize), self.base_url)
        output += '\n%s: %s' % (string.rjust(app_key, maxsize), self.app_key)
        output += '\n%s: %s' % (string.rjust(app_secret, maxsize), self.app_secret)
        output += '\n%s: %s' % (string.rjust(consumer_key, maxsize), self.consumer_key)

        return output

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
