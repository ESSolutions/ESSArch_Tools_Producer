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

from django import forms
from django.core.validators import validate_email
#from django.utils.safestring import mark_safe
#from django.forms.util import flatatt

# own models etc
from configuration.models import PlainText, Choices_DeliveryType
from profiles.models import AgentProfile, ClassificationProfile, DataSelectionProfile, ImportProfile, TransferProjectProfile 


class EmailField(forms.CharField):
    default_error_messages = {
        'invalid': (u'Enter a valid e-mail address.'),
        }
    default_validators = [validate_email]


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally instead of vertically. """
    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class PrepareFormSE(forms.Form):
#    destinationroot = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False  )
    archivist_organization = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    label = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
#    startdate = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
#    enddate = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    
class PrepareFormNO(forms.Form):
#    destinationroot = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False  )
    archivist_organization = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    label = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
#    startdate = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
#    enddate = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    
class PrepareFormEC(forms.Form):
    # enables form reload data when template is refreshed
    def __init__(self, *args, **kwargs):
        super(PrepareFormEC, self).__init__(*args, **kwargs)
        self.fields['AgentProfile'].choices = getAgentProfiles()
        self.fields['ClassificationProfile'].choices = getClassificationProfiles()
        self.fields['DataSelectionProfile'].choices = getDataSelectionProfiles()
        self.fields['ImportProfile'].choices = getImportProfiles()
        self.fields['TransferProjectProfile'].choices = getTransferProjectProfiles()

    archivist_organization = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={
                                                                                              'size':'52', 
                                                                                              'title':'The name of the archival creator of the information about to be archived.',
                                                                                              }))
    label = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={
                                                                             'size':'52',
                                                                             'title':'Archival label description of the information about to be archived',
                                                                             }))
    AgentProfile = forms.ChoiceField(widget=forms.Select(attrs={
                                                                'title':'The profile for responsible agents/organizations taking part in the archiving process',
                                                                }))
    ClassificationProfile = forms.ChoiceField(widget=forms.Select(attrs={
                                                                'title':'The information classification schema profile to be used for the information to be archived',
                                                                }))
    DataSelectionProfile = forms.ChoiceField(widget=forms.Select(attrs={
                                                                'title':'The descriptive metadata profile used for the information to be archived',
                                                                }))
    ImportProfile = forms.ChoiceField(widget=forms.Select(attrs={
                                                                'title':'The import transformation profile to be used for the information to be archived',
                                                                }))
    TransferProjectProfile = forms.ChoiceField(widget=forms.Select(attrs={
                                                                'title':'The descriptive profile of the transfer project used for the information to be archived',
                                                                }))
#    Test = forms.ChoiceField( choices=[ ( "Ok", "Ok" ),( "Failed", "Failed" ) ] )

"Get all the Agent Profiles from the database"
###############################################
def getAgentProfiles():
    AgentProfiles=[]
    objs = AgentProfile.objects.all()
    for et in objs:
        AgentProfiles.append( ( et.agent_profile_id, et.agent_profile ) )
    return AgentProfiles

def getClassificationProfiles():
    ClassificationProfiles=[]
    objs = ClassificationProfile.objects.all()
    for et in objs:
        ClassificationProfiles.append( ( et.classification_profile_id, et.classification_profile ) )
    return ClassificationProfiles

def getDataSelectionProfiles():
    DataSelectionProfiles=[]
    objs = DataSelectionProfile.objects.all()
    for et in objs:
        DataSelectionProfiles.append( ( et.data_selection_profile_id, et.data_selection_profile ) )
    return DataSelectionProfiles

def getImportProfiles():
    ImportProfiles=[]
    objs = ImportProfile.objects.all()
    for et in objs:
        ImportProfiles.append( ( et.import_profile_id, et.import_profile ) )
    return ImportProfiles

def getTransferProjectProfiles():
    TransferProjectProfiles=[]
    objs = TransferProjectProfile.objects.all()
    for et in objs:
        TransferProjectProfiles.append( ( et.transfer_project_profile_id, et.transfer_project_profile ) )
    return TransferProjectProfiles


class CreateFormSE(forms.Form):
#    destinationroot                                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    label                                            = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Label' )
    deliverytype                                     = forms.ChoiceField( choices=Choices_DeliveryType, label='Delivery type *' )
    deliveryspecification                            = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Delivery specification *' )
    submissionagreement                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submission agreement *' )
#    previoussubmissionagreement                      = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Previous submission agreement' )
#    startdate                                        = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period start date *' )
#    enddate                                          = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period end date *' )
#    startdate                                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period start date *' )
#    enddate                                          = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period end date *' )
    archivist_organization                           = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Archivist organization *' )
    archivist_organization_id                        = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }), label='Archivist organization note *' )
    archivist_organization_software                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system name *')
    creator_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Creator organization *' )


class CreateFormNO(forms.Form):
#    destinationroot                                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    label                                            = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Label' )
    submissionagreement                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submission agreement *' )
#    startdate                                        = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period start date *' )
#    enddate                                          = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period end date *' )
    startdate                                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period start date *' )
    enddate                                          = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period end date *' )
    archivist_organization                           = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Archivist organization *' )
    archivist_organization_software                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system name *')
    archivist_organization_software_id               = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system version *')
    archivist_organization_software_type             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system type *') 
    creator_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Creator organization *' )
    producer_organization                            = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer organization *' )
    producer_individual                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer individual *')
    producer_organization_software_type              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer software system type *')
    submitter_organization                           = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submitter organization *' )
    submitter_individual                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submitter individual *' )
    ipowner_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='IP owner organization *' )
    preservation_organization                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Preservation organization *' )

class CreateFormEC(forms.Form):
#    destinationroot                                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    label                                            = forms.CharField( max_length = 200, widget=PlainText(attrs={
                                                                                                                  'size':'52',
                                                                                                                  'title':'Archival label description of the information about to be archived',
                                                                                                                  }), label='Archive label' )
    deliverytype                                     = forms.ChoiceField( choices=Choices_DeliveryType, widget=forms.Select(attrs={
                                                                                                     'title':'The content type being submitted with this package',
                                                                                                     }), label='Content type *')
    submissionagreement                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={
                                                                                                                        'size':'52',
                                                                                                                        'title':'Reference to the used submission agreement',
                                                                                                                        }), label='Submission agreement' )
#    startdate                                        = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period start date *' )
#    enddate                                          = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period end date *' )
#    startdate                                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period start date *' )
#    enddate                                          = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Period end date *' )
    archivist_organization                           = forms.CharField( max_length = 200, widget=PlainText(attrs={
                                                                                                                  'size':'52',
                                                                                                                  'title':'The name of the archival creator of the information about to be archived.',
                                                                                                                  }), label='Archivist organization *' )
#    archivist_organization_software                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system name *')
#    archivist_organization_software_id               = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system version *')
#    archivist_organization_software_type             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system type *')
#    creator_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Creator organization *' )
#    producer_organization                            = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer organization *' )
#    producer_individual                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer individual *')
#    producer_organization_software_type              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer software system type *')
    submitter_organization                           = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={
                                                                                                                        'size':'52',
                                                                                                                        'title':'Name of the organization submitting the package to the archive',
                                                                                                                        }), label='Submitter organization *' )
#    submitter_individual                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submitter individual *' )
#    ipowner_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='IP owner organization *' )
    preservation_organization                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={
                                                                                                                        'size':'52',
                                                                                                                        'title':'Name of the organization preserving the package',
                                                                                                                        }), label='Preservation organization *' )


#class CreateForm(forms.Form):
    #destinationroot                                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    #objid                                           = models.CharField( max_length = 255, unique=True   ) # mandatory, automatically
    #label                                            = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Label' )
    #type                                            = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Package type' )
    #createdate                                      = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #recordstatus                                    = models.CharField( max_length = 255 )
    #deliverytype                                    = forms.ChoiceField( choices=Choices_DeliveryType, label='Delivery type *' )
    #deliveryspecification                           = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #submissionagreement                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submission agreement *' )
    #systemtype                                      = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #previoussubmissionagreement                     = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Previous submission agreement' )
    #datasubmissionsession                           = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #packagenumber                                   = models.CharField( max_length = 255 )
    #referencecode                                   = models.CharField( max_length = 255 )
    #previousreferencecode                           = models.CharField( max_length = 255 )
    #appraisal                                       = models.CharField( max_length = 255 )
    #accessrestrict                                  = models.CharField( max_length = 255 )
    #startdate                                        = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period start date *' )
    #enddate                                          = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Period end date *' )
    #informationclass                                = forms.ChoiceField( choices=[ ( "0", "0" ),( "1", "1" ) ] )
    #comments                                        = models.CharField( max_length = 255 )
    #archivist_organization                           = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='Archivist organization *' )
    #archivist_organization_id                       = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }))
    #archivist_organization_software                  = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system name *')
    #archivist_organization_software_id               = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system version *')
    #archivist_organization_software_type             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Archivist software system type *') 
    #archivist_organization_software_type_version    = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'})
    #archivist_individual                            = models.CharField( max_length = 255 )
    #archivist_individual_telephone                  = models.CharField( max_length = 255 )
    #archivist_individual_email                      = models.CharField( max_length = 255 )
    #creator_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Creator organization *' )
    #creator_organization_id                         = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )
    #creator_individual                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #creator_individual_details                      = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )  
    #creator_individual_telephone                    = models.CharField( max_length = 255 )
    #creator_individual_email                        = models.CharField( max_length = 255 )
    #creator_software                                = models.CharField( max_length = 255 )
    #creator_software_id                             = models.CharField( max_length = 255 )
    #producer_organization                            = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer organization *' )
    #producer_organization_id                        = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )
    #producer_individual                              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer individual *')
    #producer_individual_telephone                   = models.CharField( max_length = 255 )
    #producer_individual_email                       = models.CharField( max_length = 255 )
    #producer_organization_software                  = models.CharField( max_length = 255 )
    #producer_organization_software_identity         = models.CharField( max_length = 255 )
    #producer_organization_software_type              = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Producer software system type *')
    #producer_organization_software_type_version     = models.CharField( max_length = 255 )
    #submitter_organization                           = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submitter organization *' )
    #submitter_organization_id                       = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )
    #submitter_individual                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Submitter individual *' )
    #submitter_individual_telephone                  = models.CharField( max_length = 255 )
    #submitter_individual_email                      = models.CharField( max_length = 255 )
    #ipowner_organization                             = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='IP owner organization *' )
    #ipowner_organization_id                         = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )
    #ipowner_individual                              = models.CharField( max_length = 255 )
    #ipowner_individual_telephone                    = models.CharField( max_length = 255 )
    #ipowner_individual_email                        = models.CharField( max_length = 255 )
    #editor_organization                             = models.CharField( max_length = 255 )
    #editor_organization_id                          = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }) )
    #preservation_organization                        = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='Preservation organization *' )
    #preservation_organization_id                    = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "5", }))
    #preservation_organization_software              = models.CharField( max_length = 255 )
    #preservation_organization_software_id           = models.CharField( max_length = 255 )
    #aic_id                                          = models.CharField( max_length = 255 ) # mandatory, automatically
    #projectname                                     = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    #policyid                                        = forms.IntegerField(widget=forms.TextInput(attrs={'size':'10'}) )
    #policyid                                        = forms.ChoiceField( choices=[ ( "0", "0" ),( "1", "1" ),( "3", "3" ),( "4", "4" ) ] )
    #receipt_email                                   = EmailField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )

