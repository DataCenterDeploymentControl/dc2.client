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

import os
import os.path
import pickle

__all__ = ['AuthCache']

class AuthCache(object):
    def __init__(self, username=None, auth_cache_dir=None):
        self._username = username
        self._auth_cache_dir = None
        if self._username is None:
            raise ValueError('username has to be set')
        if auth_cache_dir is None:
            self._auth_cache_dir = os.path.expanduser('~/.dc2-client')
        else:
            self._auth_cache_dir = os.path.expanduser(auth_cache_dir)
        if not os.path.exists(self._auth_cache_dir):
            os.makedirs(self._auth_cache_dir)
        self._auth_cache_file = '{0}/{1}'.format(self._auth_cache_dir, self._username)

    @property
    def _check_auth_cache_file(self):
        return os.path.exists(self._auth_cache_file)

    def _write_cache_data(self, data=None):
        if data is not None:
            with open(self._auth_cache_file, 'wb') as fp:
                print('In open')
                try:
                    pickle.dump(data, fp, pickle.HIGHEST_PROTOCOL)
                except Exception as e:
                    raise(e)
                return True

    def _read_cache_data(self):
        if self._check_auth_cache_file:
            data = None
            with open(self._auth_cache_file, 'rb') as fp:
                data = pickle.load(fp)
                return data
        return None

    def get(self):
        data = self._read_cache_data()
        return data

    def store(self, data=None):
        return self._write_cache_data(data)
