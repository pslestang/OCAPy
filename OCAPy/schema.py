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


import requests
from errors import OCAPyException

class Schemas(object):
    """A set of Schema"""

    def __init__(self, base_url=None):
        self.base_url = base_url
        self.list = []

    def retrieve(self, format='json'):
        """retrieves all the schemas URL"""
        request = requests.get(self.base_url)

        if request.status_code != requests.codes.ok:
            raise OCAPyException('Unable to retrieve JSON schemas: %s' % 
                                 (request.json()['message']), request=request)

        for api in request.json()['apis']:
            self.list.append(Schema(base_url=self.base_url,
                                    path=str(api['schema']).format(path=api['path'],
                                    format=format),
                                    format=format))
        return self.list

    
class Schema(object):
    """modelizes a schema"""

    def __init__(self, base_url=None, path=None, format='json'):
        self.base_url = base_url
        self.path = path
        self.format = format
        self.content = None

    def load(self):
        url = '%s/%s' % (self.base_url.rstrip('/'), self.path.lstrip('/'))
        request = requests.get(url)

        if request.status_code != requests.codes.ok:
            raise OCAPyException('Unable to load JSON schema %s: %s' %
                                 (self.path, request.json()['message']), request=request)

        self.content = request.json()
        return self.content


if __name__ == '__main__':
    schemas = Schemas()
    schemas.base_url = 'https://api.ovh.com/1.0/'
    for schema in schemas.retrieve():
        print schema.path

# vim:set shiftwidth=4 tabstop=4 softtabstop=4 encoding=utf-8 expandtab textwidth=79

