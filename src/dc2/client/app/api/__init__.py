# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__ = 'stephan.adig'

__all__ = ['API']

import json

try:
    import requests
    from requests.auth import AuthBase
except ImportError as e:
    raise e

from ..globals import AUTH_TYPES
from .auth_cache import AuthCache

class DC2Authentication(AuthBase):
    def __init__(self, token=None, username=None):
        self._token = token
        self._username = username


    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, _username=None):
        self._username = _username

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, _token=None):
        self._token = _token

    def __call__(self, r):
        r.headers['X-DC2-Auth-Token'] = self._token
        r.headers['X-DC2-Auth-User'] = self._username
        return r


class API(object):

    HEADERS = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    # URL_FORMAT
    #   {0} = base_url
    #   {1} = module i.e. "admin"
    #   {2} = api_version

    URL_FORMAT = "{0}/{1}/{2}"

    def __init__(self, config=None):
        """
        Constructor

        :param config:
        :type config: dc2.client.configuration.Configuration Instance
        """
        if config is None:
            raise ValueError('config needs to be set')
        self._config = config.config()
        self._base_url = self._config['default']['connection']['dc2_backend_url']
        self._api_version = self._config['default']['connection']['api_version']
        self._email = self._config['default']['authentication']['email']
        self._password = self._config['default']['authentication']['password']
        self._auth_type = self._config['default']['authentication']['auth_method']
        self._auth_cache_dir = self._config['default']['authentication']['auth_cache_dir']
        self._authenticated = False
        self._auth_cache = AuthCache(self._email, self._auth_cache_dir)
        self._auth = None

    def _login(self):
        if self._email is None or self._password is None:
            raise ValueError('email and/or password need to be set when doing a login')
        if self._auth_type in AUTH_TYPES:
            login_rec = AUTH_TYPES[self._auth_type](self._email, self._password)
            if login_rec is not None:
                base = self.URL_FORMAT.format(self._base_url, 'auth', self._api_version)
                url = "{0}/{1}".format(base,'login')
                response = requests.post(url, data=json.dumps(login_rec),headers=self.HEADERS)
                if response is not None:
                    if response.status_code > 400:
                        self._authenticated = False
                        return False
                    elif response.status_code == 200:
                        token = response.headers.get('X-DC2-Auth-Token')
                        username = response.headers.get('X-DC2-Auth-User')
                        if self._auth is None:
                            self._auth = DC2Authentication(token, username)
                        else:
                            self._auth.username = username
                            self._auth.token = token

                        self._auth_cache.store(self._auth)
                        self._authenticated = True
                        return True
        return False


    def url(self, module=None, resource=None):
        if module is not None and resource is not None:
            base = self.URL_FORMAT.format(self._base_url, module, self._api_version)
            resource = "{0}/{1}".format(base, resource)
            return resource
        return None

    def _check_authentication(self):
        if not self._authenticated and self._auth is None:
            return self._login()
        elif self._authenticated and self._auth is None:
            return self._login()
        elif self._authenticated and self._auth is not None:
            return True
        else:
            return False

    def do_request(self, url=None, method="GET", data=None, auth=False):
        if url is not None:
            response = None
            extras = {}
            if auth:
                auth_obj = self._auth_cache.get()
                if auth_obj is None:
                    self._authenticated = False
                    self._auth = None
                    self._check_authentication()
                else:
                    self._auth = auth_obj
            request_done = False
            while not request_done:
                if method.lower() == 'get':
                    response = requests.get(url, params=data, auth=self._auth, headers=self.HEADERS)
                if method.lower() == 'post':
                    response = requests.post(url, data=json.dumps(data), auth=self._auth, headers=self.HEADERS)
                if method.lower() == 'put':
                    pass
                if method.lower() == 'delete':
                    response = requests.delete(url, data=json.dumps(data), auth=self._auth, headers=self.HEADERS)
                if response.status_code == 401:
                    if auth:
                        self._authenticated = False
                        self._auth = None
                        self._check_authentication()
                elif 200 <= response.status_code < 300:
                    request_done = True
                    return response.json()
                else:
                    # TODO: Return error
                    request_done = True
                    return response.json()
            return response
        return None
