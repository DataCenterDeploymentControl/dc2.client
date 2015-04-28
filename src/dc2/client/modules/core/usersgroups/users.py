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

try:
    import requests
except ImportError as e:
    raise e


class Users(object):

    _MODULE_NAME_ = 'admin'
    _RESOURCE_NAME = 'users'

    def __init__(self, api=None):
        if api is None:
            raise ValueError('api instance can not be None')
        self._api = api
        self._url = self._api.url(self._MODULE_NAME_, self._RESOURCE_NAME)

    def userlist(self, username=None, email=None):
        response = None
        if username is not None and email is None:
            response = self._api.do_request(self._url, 'GET', data={'username': username}, auth=True)
        elif username is None and email is not None:
            response = self._api.do_request(self._url, 'GET', data={'email': email}, auth=True)
        else:
            response = self._api.do_request(self._url, 'GET', auth=True)
        if response is not None:
            return True, response
        else:
            return False, 'Error'

    def useradd(self, user_rec=None):
        if user_rec is not None:
            response = self._api.do_request(self._url, 'POST', data=user_rec, auth=True)
            return response
