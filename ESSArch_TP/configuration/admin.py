#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
"""
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
"""

from configuration.models import Parameter, Path, Schema, EventType, Agent
from django.contrib import admin


"""
Parameters for configuration options
"""
class ParameterAdmin( admin.ModelAdmin ):
    list_display = ( 'entity', 'value' )
    search_fields = ( 'entity', )
    readonly_fields = ('entity',)
    fields = ('entity', 'value')

admin.site.register(Parameter, ParameterAdmin)


"""
Paths used for different operations
"""
class PathAdmin( admin.ModelAdmin ):
    list_display = ( 'entity', 'value' )
    search_fields = ( 'entity', )
    readonly_fields = ('entity',)
    fields = ('entity', 'value')

admin.site.register(Path, PathAdmin)


"""
XML schemas and namespaces
"""
class SchemaAdmin( admin.ModelAdmin ):
    list_display = ( 'entity', 'value' )
    search_fields = ( 'entity', )
    readonly_fields = ('entity',)
    fields = ('entity', 'value')

admin.site.register(Schema, SchemaAdmin)


"""
Event types
"""
class EventTypeAdmin( admin.ModelAdmin ):
    list_display = ( 'eventDetail', 'eventType' )
    search_fields = ( 'eventDetail', )

admin.site.register( EventType, EventTypeAdmin )


"""
Agents used for different operations
"""
class AgentAdmin( admin.ModelAdmin ):
    list_display = ( 'agentDetail', 'agentType' )
    search_fields = ( 'agentDetail', )
    readonly_fields = ('agentDetail',)
    fields = ('agentType', 'agentDetail')

admin.site.register(Agent, AgentAdmin)


