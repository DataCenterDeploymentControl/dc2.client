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


__all__ = ['Configuration']


try:
    import yaml
except ImportError as e:
    raise e

import os
import os.path


class Configuration(object):
    """
    Class: Configuration
    Purpose:
        An instance of this class will load one or many configuration files and provides
        access to the configuration settings from the Application.
    """
    def __init__(self, filenames=None):
        """
        Initialize the Configuration Object
        :param list filenames:
        :return: instance of class Configuration
        """
        self._filenames = []
        self._can_load = False
        self._configuration = {}
        if filenames is not None:
            self._filenames = filenames
        if len(self._filenames) > 0:
            self._can_load = True
            self._load_config()

    def _load_config(self):
        """
        Private

        Loads the configuration files in order of the filename list.
        """
        if self._can_load:
            content_buffer = {}
            configuration = {}
            for filename in self._filenames:
                if os.path.exists(filename):
                    with open(filename, 'rb') as fp:
                        content_buffer[filename] = fp.read()
                    configuration.update(yaml.load(content_buffer[filename]))
            self._configuration = configuration

    def set_filenames(self, filenames=[]):
        if len(filenames) > 0:
            self._filenames = filenames
            self._can_load = True
            self._load_config()

    def get_filenames(self):
        return self._filenames
    filenames = property(get_filenames, set_filenames)

    def config(self):
        return self._configuration