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

try:
    from pkg_resources import iter_entry_points
except ImportError as e:
    raise e

from dc2.client.cli import PARSER
from .globals import DC2_EXTERNAL_CLIENT_MODULES
from .globals import CONFIGURATION

def main():
    create_argparser()
    _load_external_modules()
    _init_external_modules()
    args = PARSER.parse_args()
    result = args.func(args)
    if args.config_file is not None:
        pass
    elif os.path.exists(os.path.expanduser('~/.dc2-client.cfg')):
        pass
    else:
        pass
    if result is False:
        return(-1)


def _load_external_modules():
    print('Loading Modules...')
    for entry in iter_entry_points('dc2.client.modules', name=None):
        print('Loading {0}'.format(entry.name))
        DC2_EXTERNAL_CLIENT_MODULES.append(entry.load())


def _init_external_modules():
    for module in DC2_EXTERNAL_CLIENT_MODULES:
        module()


def create_argparser():
    PARSER.add_argument(
        '--dc2-backend-url',
        action="store",
        dest="dc2_backend_url",
        default="http://localhost:5000/api",
        required=True,
        metavar="URL",
        help="DC2 Backend URL")
    PARSER.add_argument(
        '-C',
        '--config-file',
        action='store',
        dest="config_file",
        default=None,
        required=False,
        metavar='FILE',
        help="Configuration File"
    )
