#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Copyright 2013 Pierre-Samuel Le Stang (ps@lestang.fr)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

class OCAPyException(Exception):
    """Defines the exception base class for OCAPy classes"""

    def __init__(self, message, request=None):
        Exception.__init__(self, message)
        self.request=request

class OCAPyConfigException(Exception):
    """Defines the exception class for OCAPy Config classes"""
    pass

class OCAPyInputException(Exception):
    """Defines the exception class for OCAPy Config classes"""
    pass

# vim:set shiftwidth=4 tabstop=4 softtabstop=4 encoding=utf-8 expandtab textwidth=79

