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

__all__ = ['PARSER', 'SUBPARSERS', 'output', 'DC2_EXTERNAL_CLIENT_MODULES', 'CONFIG']
import os
import os.path

try:
    from pkg_resources import iter_entry_points
except ImportError as e:
    raise e

from dc2.client.cli import PARSER, SUBPARSERS, output, OUTPUT_FORMATS
from .globals import DC2_EXTERNAL_CLIENT_MODULES
from .globals import CONFIG
from .globals import AUTH_TYPES

from .api import API

def main():
    create_argparser()
    args = PARSER.parse_args()
    api = None
    if args.config_file is not None:
        CONFIG.set_filenames([args.config_file])
    else:
        CONFIG.set_filenames(['default.yaml', os.path.expanduser('~/.dc2-client/default.yaml')])
        api = API(CONFIG)
    result = args.func(args, api)
    if result is False:
        return(-1)


def create_argparser():
    PARSER.add_argument(
        '--dc2-backend-url',
        action="store",
        dest="dc2_backend_url",
        default="http://localhost:5000/api",
        required=False,
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
    PARSER.add_argument(
        '--format',
        action="store",
        dest='output_format',
        default="text",
        required=False,
        choices=OUTPUT_FORMATS.keys(),
        metavar="{0}".format([key for key in OUTPUT_FORMATS.keys()]),
        help='Choose the output format'

    )
