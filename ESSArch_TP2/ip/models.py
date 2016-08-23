"""
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2016  ES Solutions AB

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

# Create your models here.
from django.db import models

import uuid

"""
Informaion Package
"""
class InformationPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # ObjectUUID
    Producer		= models.CharField( max_length = 255 )
    Label		= models.CharField( max_length = 255 )
    Content		= models.CharField( max_length = 255 )
    Responsible		= models.CharField( max_length = 255 )
    CreateDate		= models.CharField( max_length = 255 )
    State		= models.CharField( max_length = 255 )
    Status		= models.CharField( max_length = 255 )
    ObjectSize		= models.CharField( max_length = 255 )
    ObjectNumItems	= models.CharField( max_length = 255 )
    ObjectPath		= models.CharField( max_length = 255 )
    Startdate		= models.CharField( max_length = 255 )
    Enddate		= models.CharField( max_length = 255 )
    OAIStype		= models.CharField( max_length = 255 )
#    ObjectIdentifierValue	= models.CharField( max_length = 255 )
#    ObjectPackageName		= models.CharField( max_length = 255 )
#    ObjectMessageDigestAlgorithm	= models.CharField( max_length = 255 )
#    ObjectMessageDigest		= models.CharField( max_length = 255 )
#    ObjectActive		= models.CharField( max_length = 255 )
#    MetaObjectIdentifier	= models.CharField( max_length = 255 )
#    MetaObjectSize		= models.CharField( max_length = 255 )
#    CMetaMessageDigestAlgorithm	= models.CharField( max_length = 255 )
#    CMetaMessageDigest		= models.CharField( max_length = 255 )
#    PMetaMessageDigestAlgorithm	= models.CharField( max_length = 255 )
#    PMetaMessageDigest		= models.CharField( max_length = 255 )
#    DataObjectSize		= models.CharField( max_length = 255 )
#    DataObjectNumItems		= models.CharField( max_length = 255 )
#    Status			= models.CharField( max_length = 255 )
#    StatusActivity		= models.CharField( max_length = 255 )
#    StatusProcess		= models.CharField( max_length = 255 )
#    LastEventDate		= models.CharField( max_length = 255 )
#    linkingAgentIdentifierValue	= models.CharField( max_length = 255 )
#    CreateAgentIdentifierValue	= models.CharField( max_length = 255 )
#    EntryDate			= models.CharField( max_length = 255 )
#    preservationLevelValue	= models.CharField( max_length = 255 )
#    Informationclass		= models.CharField( max_length = 255 )
#    Generation			= models.CharField( max_length = 255 )
#    LocalDBdatetime		= models.CharField( max_length = 255 )
#    ExtDBdatetime		= models.CharField( max_length = 255 )
#    PolicyId			= models.CharField( max_length = 255 )
#    ObjectMetadata_id		= models.CharField( max_length = 255 )

    class Meta:
        ordering = ["id"]
        verbose_name = 'Information Package'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s' % self.id

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in InformationPackage._meta.fields }


"""
Events related to IP
"""
class EventIP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # eventIdentifierValue
    eventType = models.ForeignKey(
        'configuration.EventType',
        on_delete=models.CASCADE
    )
    eventDateTime		= models.CharField( max_length = 255 )
    eventDetail			= models.CharField( max_length = 255 )
    eventApplication		= models.CharField( max_length = 255 )
    eventVersion		= models.CharField( max_length = 255 )
    eventOutcome		= models.CharField( max_length = 255 )
    eventOutcomeDetailNote	= models.CharField( max_length = 1024 )
    linkingAgentIdentifierValue	= models.CharField( max_length = 255 )
    linkingObjectIdentifierValue = models.ForeignKey(
        'InformationPackage',
        on_delete=models.CASCADE,
        related_name='events'
    )

    class Meta:
        ordering = ["eventType"]
        verbose_name = 'Events related to IP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s' % self.id

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return { field.name: field.value_to_string(self)
                 for field in EventIP._meta.fields }

