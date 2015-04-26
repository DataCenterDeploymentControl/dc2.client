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

__all__ = ['load_external_modules', 'init_external_modules']

try:
    from pkg_resources import iter_entry_points
except ImportError as e:
    raise e


def load_external_modules():
    print('Loading Modules...')
    external_modules = []
    for entry in iter_entry_points('dc2.client.modules', name=None):
        print('Loading {0}'.format(entry.name))
        external_modules.append(entry.load())
    return external_modules


def init_external_modules(external_modules=[]):
    for module in external_modules:
        module()