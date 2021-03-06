#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Programming contest management system
# Copyright © 2013 Bernard Blackham <b-cms@largestprime.net>
# Copyright © 2010-2012 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2012 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
# Copyright © 2018 Louis Sugy <contact@nyri0.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from cms import config


logger = logging.getLogger(__name__)


def get_all_auth_types():
    auth_types = []
    for auth_type_name in config.auth_types:
        try:
            auth_types.append(get_auth_type(auth_type_name))
        except KeyError:
            logger.warning("Authentication type '%s' not found."
                           % auth_type_name)
            pass

    return auth_types


def get_auth_type(auth_type_name=None):
    """Given an auth type name, find the corresponding AuthType class.

    auth_type_name (string): if we only need the class, we can
                             give only the auth type name.

    return (object): an instance of the correct AuthType class.
    """
    mod = __import__('cms.server.authtypes.%s' % auth_type_name.lower(),
                     globals(), locals(), [auth_type_name], 0)
    return mod.__dict__[auth_type_name]


def get_auth_details(user):
    try:
        auth_type = get_auth_type(config.auth_types[0])
    except KeyError:
        return ""

    return auth_type.get_user_string(user)
