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
    from requests.auth import AuthBase
except ImportError as e:
    raise(e)

__all__ = ['LocalAuth']

from ..auth_types import register_auth_methods


def local_login(email=None, password=None):
    if email is not None and password is not None:
        login = {
            'email': email,
            'password': password,
            'auth_type': 'local'
        }
        return login
    return None


class LocalAuth(AuthBase):
    def __init__(self, token=None, username=None):
        self._token = token
        self._username = username

    def __call__(self, r):
        r.headers['X-DC2-Auth-Token'] = self._token
        r.headers['X-DC2-Auth-Username'] = self._username
        return r

register_auth_methods('local', local_login)