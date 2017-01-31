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
"""
WSGI config for ESSArch TP.
"""
import os, sys, platform

# Activate virtualenv before any imports
# if platform.system() != 'Linux' :
#     activate_this = '/ESSArch/env/Scripts/activate_this.py'
#     execfile(activate_this, dict(__file__=activate_this))
#     sys.path.append('/ESSArch/etp')
# else:
sys.path.append('/ESSArch/pd/python/lib/python2.7/site-packages/ESSArch_TP')
sys.path.append('/ESSArch/config')
    #sys.path.append('/ESSArch/etp') # append path

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
