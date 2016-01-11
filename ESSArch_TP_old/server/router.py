#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
'''
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2013  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
'''

class serverRouter(object):
    """
    A router to control all database operations on models in
    the server application
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on 'server' models to 'essarch_local'
        """
        if model._meta.app_label == 'server':
            return 'essarch_local'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on 'server' models to 'essarch_local'
        """
        if model._meta.app_label == 'server':
            return 'essarch_local'
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'server' app only appears on the 'essarch_local' db
        """
        if db == 'essarch_local':
            return model._meta.app_label == 'server'
        elif model._meta.app_label == 'server':
            return False
        return None

