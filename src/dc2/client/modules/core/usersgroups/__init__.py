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

from .users import Users
from dc2.client.cli import output


def create_parser(subparser=None):
    if subparser is None:
        raise ValueError('subparser can not be None')
    users_parser = subparser.add_parser(
        'users',
        description="User Administration Tool",
        help="Administrate your local users of DC2"
    )
    users_parser.add_argument(
        '--list',
        action="store_true",
        dest="user_list",
        default=False,
        help="List Users"
    )
    user_list = users_parser.add_argument_group('list', 'All list user options')
    user_list.add_argument(
        '--find-username',
        action="store",
        default=None,
        dest="user_username",
        metavar="USERNAME",
        help='Find User by Username'
    )
    user_list.add_argument(
        '--find-email',
        action="store",
        default=None,
        dest="user_email",
        metavar="EMAIL ADDRESS",
        help="Find User by eMail"
    )
    users_parser.set_defaults(parser_name="users", func=process_users)


def process_users(args=None, api=None):
    if args is None:
        raise ValueError('args can not be None')
    if args.parser_name == 'users':
        ctl_users = Users(api)
        print(ctl_users)
        if args.user_list:
            if args.user_username is None is args.user_email is None:
                (result, response) = ctl_users.userlist()
                output(result, response, format=args.output_format)


