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

# own models etc
from configuration.models import PlainText

class DeliverForm(forms.Form):
    #destination = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}) )
    #destination = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}) )
    preservation_organization_url  = forms.URLField( max_length = 400, widget=PlainText(attrs={'size':'52'}), label='Receiver', required=False )
    #username    = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}))
    #password    = forms.CharField( max_length = 200, label="Destination Root", widget=forms.TextInput(attrs={'size':'52'}))

    email_from = forms.CharField( max_length = 200, widget=PlainText(attrs={'size':'52'}), label='From:', required=False ) 
    email_to = forms.CharField( max_length = 200, widget=forms.TextInput(attrs={'size':'52'}), label='To: *'  ) 
    email_subject = forms.CharField(widget=forms.TextInput(attrs={'size':'52'}), label='Subject *' )
    email_body = forms.CharField( widget=forms.Textarea(attrs={'width':"100%", 'cols' : "50", 'rows': "5", }), label='Body *' )
    
