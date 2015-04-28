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


from .groups import Groups
from dc2.client.cli import output


def group_parser(parser=None):

    groups_action_group = parser.add_mutually_exclusive_group()
    groups_action_group.add_argument(
        '--list',
        action="store_true",
        dest="group_list",
        default=False,
        help="List Users"
    )
    groups_action_group.add_argument(
        '--add',
        action="store_true",
        dest="group_add",
        default=False,
        help="Add User"
    )
    groups_action_group.add_argument(
        '--new',
        action="store_true",
        dest="group_new",
        default=False,
        help="New User Record"
    )
    groups_action_group.add_argument(
        '--delete',
        action="store",
        dest="group_delete",
        default=None,
        metavar="USERNAME or EMAIL",
        help="Delete User Record"
    )
    group_list = parser.add_argument_group('list', 'All "User List" options')
    group_list.add_argument(
        '--groupname',
        action="store",
        dest="group_groupname",
        default=None,
        metavar="GROUPNAME",
        help="List Group by Groupname"
    )
    group_add = parser.add_argument_group('add', 'All "Group Add" options')
    group_add.add_argument(
        '--group-file',
        action="store",
        dest="group_file",
        default=None,
        metavar="FILENAME",
        help="Group JSON File"
    )

    # user_list.add_argument(
    #     '--find-username',
    #     action="store",
    #     default=None,
    #     dest="user_username",
    #     metavar="USERNAME",
    #     help='Find User by Username'
    # )
    # user_list.add_argument(
    #     '--find-email',
    #     action="store",
    #     default=None,
    #     dest="user_email",
    #     metavar="EMAIL ADDRESS",
    #     help="Find User by eMail"
    # )
    # user_add = parser.add_argument_group('add', 'All "add user" options')
    # user_add.add_argument(
    #     '--users-file',
    #     action="store",
    #     dest="users_add_file",
    #     default=None,
    #     metavar="FILENAME",
    #     help="Add users from file"
    # )
    parser.set_defaults(parser_name="groups", func=process_groups)


def process_groups(args=None, api=None):
    if args is None:
        raise ValueError('args can not be None')
    if args.parser_name == 'groups':
        ctl_groups = Groups(api)
        if args.group_list:
            response = None
            result = False
            if args.group_groupname is not None:
                result, response = ctl_groups.grouplist(groupname=args.group_groupname)
            else:
                result, response = ctl_groups.grouplist()
            output(result, response, format=args.output_format)
        elif args.group_new:
            group_rec = {
                'groupname': '<groupname, required>',
                'desc': '<optional, Human Readable description of the group'
            }
            output(True, group_rec, format="json")

        elif args.group_add:
            if args.group_file is not None:
                if os.path.exists(args.group_file):
                    with open(args.group_file, 'rb') as fp:
                        json_blob = fp.read()
                        import json
                        try:
                            groups = json.loads(json_blob.decode('utf-8'))
                            if isinstance(groups, list):
                                group_recs = []
                                for group in groups:
                                    result, response = ctl_groups.groupadd(group_rec=group)
                                    if 'error' not in response:
                                        group_recs.append({
                                            'groupname': response['group']['groupname'],
                                            'desc': response['group']['descr']
                                        })
                                    else:
                                        response.update({'group': group})
                                        output(False, response, format="json")

                                output(True, group_recs, format="json")
                            else:
                                result, response = ctl_groups.groupadd(group_rec=groups)
                                if 'error' not in response:
                                    output(True, {
                                        'groupname': response['group']['groupname'],
                                        'desc': response['group']['descr']
                                    })
                                    return
                                else:
                                    output(False, response, format="json")
                                    return
                        except ValueError as e:
                            for i in e.args:
                                output(False, i, format="text")
        elif args.group_delete is not None:
            result, response = ctl_groups.groupdelete(groupname=args.group_delete)
            if result is not None:
                output(result, response, format="json")

    #     elif args.user_delete is not None:
    #         result = None
    #         result, response = ctl_users.userdelete(user_id=args.user_delete)
    #         if result is not None:
    #             output(result, response, format="json")
