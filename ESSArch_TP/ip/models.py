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

# Create your models here.
from django.db import models


class InformationPackage(models.Model):
    #creator         = models.CharField( max_length = 255 )
    archivist_organization  = models.CharField( max_length = 255 )
    label                   = models.CharField( max_length = 255 )
#    startdate               = models.CharField( max_length = 255 )
#    enddate                 = models.CharField( max_length = 255 )
    createdate              = models.CharField( max_length = 255 )
    iptype                  = models.CharField( max_length = 255 )
    uuid                    = models.CharField( max_length = 255 )
    directory               = models.CharField( max_length = 255 )
    site_profile            = models.CharField( max_length = 255 )
    state                   = models.CharField( max_length = 255 )
    zone                    = models.CharField( max_length = 70 )
    progress                = models.IntegerField()
    class Meta:
        permissions = (
            ("Can_view_ip_menu", "Can_view_ip_menu"),
        )

    # states:
    #    - prepared
    #    - creating
    #    - created
    #    - delivered
    #    - failed
    # ?




