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
    users_action_group = users_parser.add_mutually_exclusive_group()

    users_action_group.add_argument(
        '--list',
        action="store_true",
        dest="user_list",
        default=False,
        help="List Users"
    )
    users_action_group.add_argument(
        '--add',
        action="store_true",
        dest="user_add",
        default=False,
        help="Add User"
    )
    users_action_group.add_argument(
        '--new',
        action="store_true",
        dest="user_new",
        default=False,
        help="New User Record"
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
    user_add = users_parser.add_argument_group('add', 'All "add user" options')
    user_add.add_argument(
        '--users-file',
        action="store",
        dest="users_add_file",
        default=None,
        metavar="FILENAME",
        help="Add users from file"
    )
    users_parser.set_defaults(parser_name="users", func=process_users)


def process_users(args=None, api=None):
    if args is None:
        raise ValueError('args can not be None')
    if args.parser_name == 'users':
        ctl_users = Users(api)
        if args.user_list:
            response = None
            result = False
            if args.user_username is not None and args.user_email is None:
                result, response = ctl_users.userlist(username=args.user_username)
            elif args.user_username is None and args.user_email is not None:
                result, response = ctl_users.userlist(email=args.user_email)
            else:
                result, response = ctl_users.userlist()
            output(result, response, format=args.output_format)
        if args.user_add:
            if args.users_add_file is not None:
                if os.path.exists(args.users_add_file):
                    with open(args.users_add_file, 'rb') as fp:
                        json_blob = fp.read()
                        import json
                        try:
                            user_records = json.loads(json_blob.decode('utf-8'))
                            user_recs = []
                            for user in user_records:
                                response = ctl_users.useradd(user_rec=user)
                                user_recs.append({'username': response['user']['username'], 'password': response['password']})
                            output(True, user_recs, format="json")
                        except ValueError as e:
                            for i in e.args:
                                output(False, i, format="text")
        if args.user_new:
            user_record = {
                'username': '<username>',
                'email': '<email address>',
                'name': '<Name of the User',
                'password': '<optional, remove this key and a password will be generated for you>',
                'groups': ['<optional>','remove this key and the user will have no groups, or add an array with groupnames'] ,
            }
            output(True, user_record, format='json')
