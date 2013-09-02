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


import logging
import base64
import hashlib
import time
import urllib

import requests
from requests.auth import AuthBase

# Current logger
logging.basicConfig(level=logging.INFO)

# Set urllib3/requests logging level to warning
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Authentication class which inherit from requests.aut.AuthBase
# requests module usage only
class OVHAuth(AuthBase):
    """ OVH's API authentication schema """

    def __init__(self, consumer_key=None, app_secret=None, app_key=None,
                 base_url=None, time_path='auth/time', url_path='/',
                 request_type='GET'):
        self.consumer_key=consumer_key
        self.app_key=app_key
        self.app_secret=app_secret
        self.base_url=base_url
        self.url_path=url_path
        self.request_type=request_type
        self.time_path=time_path
        self.time_url= '%s/%s' % (str(self.base_url).rstrip('/'),
                                  str(self.time_path).lstrip('/'))
        self.url='%s/%s' % (str(self.base_url).rstrip('/'),
                            str(self.url_path).lstrip('/'))

    # Compute the request signature
    # Refer to http://www.ovh.com/fr/g934.premiers-pas-avec-l-api 
    def signature(self, timestamp=None):

        if timestamp is None:
            timestamp=self.now()

        sha1=hashlib.sha1()
        sha1.update('+'.join([self.app_secret, self.consumer_key,
                              str(self.request_type).upper(), self.url, "", timestamp]))
        return '$1$'+sha1.hexdigest()

    # time is needed to sign the requests
    # Use the URL given by OVH to retrieve time
    def server_time(self):
        req = requests.get(self.time_url)
        if req.status_code != requests.codes.ok:
            raise(Exception("Time request error %s" % req.text))
        return int(requests.get(self.time_url).text)

    # Return the time difference between OVH and local time
    def drift_time(self):
        return self.server_time() - int(time.time())


    # Return the current time, taking care of drift time
    def now(self):
        return str(int(time.time()) + self.drift_time())

    # Make the class callable
    # rhe r argument is given by requests module
    def __call__(self, r):

        timestamp = self.now()
        r.headers['X-Ovh-Consumer']=self.consumer_key
        r.headers['X-Ovh-Application']=self.app_key
        r.headers['X-Ovh-Signature']=self.signature(timestamp=timestamp)
        r.headers['X-Ovh-Timestamp']=str(timestamp)

        return r


# Resource class described by:
    # 1. name: the name of the resource (ex: server)
    # 2. path: the full path to access to the resource (ex: https://api.ovh.com/1.0/dedicated/server)
    # 3. api: the api object related to the resource
    # 4. callable: the class to call that permit method chaining ( api.me.ovhAccount('FR').creditOrder )
class Resource(object):
    def __init__(self, name=None, path=None, api=None, callable=None):
        self.name = name
        self.path=path
        self.api=api
        self.callable = callable

    def __call__(self, *args, **kwargs):
        # /dedicated/server/ns1234.ovh.net => dedicated.server("ns1234.ovh.net')
        if len(args) == 1:
            # quote the arg to handle such data: 'a.b.c.d/32'
            return getattr(self, urllib.quote_plus(args[0]))

        # default call is a get()
        return self.get()

    def __getattr__(self, name):
        logging.debug("getattr called for attribute %s" % name)
        path='%s/%s' % (self.path.rstrip('/'), name)
        return self.callable(name=name,
                             api=self.api,
                             path=path,
                             callable=self.callable)

    # The common request method called by get, put, post, delete methods
    # This method return a requests instance or raise an exception if request
    # fail (return code != requests.codes.ok )
    def _request(self, type='GET', kwargs=None):

        url='%s/%s' %(self.api.base_url.rstrip('/'), self.path.lstrip('/'))
        # method: get/post/put/delete
        method=str(type).lower()

        logging.debug("%s %s" % (method, url))
        logging.debug("path is %s" % self.path)

        # call requests
        response=getattr(requests, method)(url,
                                           auth=self.api.auth(
                                               url_path=self.path,
                                               consumer_key=self.api.consumer_key,
                                               app_key=self.api.app_key,
                                               app_secret=self.api.app_secret,
                                               base_url=self.api.base_url,
                                               request_type=method
                                           ),
                                           **kwargs)

        # check the response, and raise the exception in case of non ok HTTP code
        if response.status_code != requests.codes.ok:
            raise Exception("%s %s [%s]: %s" %
                            (type.upper(), response.url, response.status_code,
                             response.json()['message']))
        else:
            return response.json()


    def get(self, **kwargs):
        logging.debug("GET request")
        return self._request(type='GET', kwargs=kwargs)

    def put(self, **kwargs):
        logging.debug("PUT request")
        return self._request(type='PUT', kwargs=kwargs)

    def post(self, **kwargs):
        logging.debug("POST request")
        return self._request(type='POST', kwargs=kwargs)

    def delete(self, **kwargs):
        logging.debug("DELETE request")
        return self._request(type='DELETE', kwargs=kwargs)

class API(object):
    def __init__(self, auth=None, base_url=None, app_key=None, app_secret=None,
                consumer_key=None):
        self.base_url=base_url
        self.auth=auth
        self.app_key=app_key
        self.app_secret=app_secret
        self.consumer_key=consumer_key

    # Dynamic building of resource
    def __getattr__(self, attribute):
        path='/%s' % attribute
        return Resource(name=attribute, api=self, path=path, callable=Resource)

class OCAPy(API):
    def __init__(self, **kwargs):
        super(OCAPy, self).__init__(auth=OVHAuth, **kwargs)

    def get_schema(self):
        pass
