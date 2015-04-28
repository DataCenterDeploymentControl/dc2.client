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

__all__ = ['create_parser']
import os
import os.path

from .userparser import user_parser
from .groupparser import group_parser


def create_parser(subparser=None):
    if subparser is None:
        raise ValueError('subparser can not be None')
    users_parser = subparser.add_parser(
        'users',
        description="User Administration Tool",
        help="Administrate your local users of DC2"
    )
    groups_parser = subparser.add_parser(
        'groups',
        description="Group Administration Tool",
        help="Administrate your local groups of DC2"
    )
    user_parser(users_parser)
    group_parser(groups_parser)
