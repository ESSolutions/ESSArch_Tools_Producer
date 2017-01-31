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
from django.utils.safestring import mark_safe

# own models etc
from configuration.models import LogEvent, PlainText, Choices_DeliveryType


#class ControlAreaForm_file():
#    #ObjectIdentifierValue = forms.CharField(label='ObjectIdentifierValue',required=False, widget = forms.HiddenInput())
#    FileSelect_CHOICES = ()
#    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxSelectMultiple())
#    def __init__(self, *args, **kwargs):
#        super(ControlAreaForm_file, self ).__init__(*args, **kwargs)
#        if self.FileSelect_CHOICES:
#            self.fields['filename'].choices = self.FileSelect_CHOICES



class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally instead of vertically. """
    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class NewLogEventForm(forms.Form):
    # enables form reload data when template is refreshed
    def __init__(self, *args, **kwargs):
        super(NewLogEventForm, self).__init__(*args, **kwargs)
        self.fields['eventType'].choices = geteventtypes()
        
    # get all the event types from the database
#    eventtypes=[]
#    objs = LogEvent.objects.all()
#    for et in objs:
#        eventtypes.append( ( et.eventType, et.eventDetail ) )
    
    eventType = forms.ChoiceField()
    eventOutcome = forms.ChoiceField( choices=[ ( "Ok", "Ok" ),( "Failed", "Failed" ) ] )
    #eventOutcome = forms.IntegerField( widget=forms.TextInput(attrs={'size':'10'}) )
    #eventOutcome = forms.IntegerField( widget=forms.TextInput(attrs={'size':'10'}) )
    #eventOutcomeDetailNote = forms.CharField( max_length = 255, widget=forms.TextInput(attrs={'size':'60'}) )
    eventOutcomeDetailNote = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "52", 'rows': "3", }))
    #linkingAgentIdentifierValue = forms.CharField( max_length = 45, widget=forms.TextInput(attrs={'size':'30'}) )
    # linkingObjectIdentifierValue = forms.CharField( max_length = 255, widget=forms.TextInput(attrs={'size':'60'}) )


"Get all the event types from the database"
###############################################
def geteventtypes():
    eventtypes=[]
    objs = LogEvent.objects.all()
    for et in objs:
        eventtypes.append( ( et.eventType, et.eventDetail ) )
    return eventtypes


class NewLogFileForm(forms.Form):
    #FileSelect_CHOICES = ()
    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxSelectMultiple())
    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.RadioSelect(), required=False)
    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.RadioSelect(), required=False)
    #filename = forms.ChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxInput(), required=False)
    #filename = forms.CheckboxSelectMultiple(choices=FileSelect_CHOICES, widget=forms.RadioSelect,required=False)
    #def __init__(self, *args, **kwargs):
    #    super(NewLogFileForm, self ).__init__(*args, **kwargs)
    #    if self.FileSelect_CHOICES:
    #        self.fields['filename'].choices = self.FileSelect_CHOICES
    
    # get info from specification file or enter manually
    #sourceroot = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False)
    #sourceroot = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}))
#    creator   = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}),required=False)
    #archivist_organization   = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}),required=False)
    #label     = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    #startdate = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    #enddate   = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), required=False )
    #iptype    = forms.ChoiceField( choices=[ ( "SIP", "SIP" ),( "AIU", "AIU" ) ], required=False  )
    #iptype    = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'10'}), required=False )

    package_description         = forms.ChoiceField( choices=(('Yes','Yes'),('No','No')), widget=forms.RadioSelect(renderer=HorizRadioRenderer), required=False)
    package_content             = forms.ChoiceField( choices=(('Yes','Yes'),('No','No')), widget=forms.RadioSelect(renderer=HorizRadioRenderer), required=False)
    #deliverytype_description    = forms.ChoiceField( choices=(('Yes','Yes'),('No','No')), widget=forms.RadioSelect(renderer=HorizRadioRenderer), required=False)

    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxSelectMultiple())
    #filename = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)
    #filename = forms.ChoiceField( choices=Choices_FileSelect, widget=forms.CheckboxInput, required=False)
    #filename = forms.ChoiceField( choices=FileSelect_CHOICES, widget=forms.RadioSelect(renderer=HorizRadioRenderer), required=False)
    #filename = forms.ChoiceField(choices=(('Yes','Yes'),('No','No')), widget=forms.CheckboxInput, required=False)
    #filename = forms.BooleanField(required=False)
    #filename = forms.MultipleChoiceField(choices=FileSelect_CHOICES, widget=forms.CheckboxSelectMultiple())
    