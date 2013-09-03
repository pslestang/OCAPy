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

# OCAPY Exceptions are raised on HTTP requests
# we let the request instance be passed to the __init__
# to help in further investigation
class OCAPyException(Exception):
    """ OCAPy exception base class """
    def __init__(self, message, request=None):
        Exception.__init__(self, message)
        self.request=request

# vim:set shiftwidth=4 tabstop=4 softtabstop=4 encoding=utf-8 expandtab textwidth=79

