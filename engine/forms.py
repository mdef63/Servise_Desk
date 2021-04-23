# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError

from .models import *


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description',  'priority', 'email_address', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'email_address': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Ticket.objects.filter(slug__exact=new_slug).count():
            raise ValidationError('Slug "{}" already exist'.format(new_slug))
        return new_slug


class UpdatedTicketForm(forms.ModelForm):

    class Meta:
        model = UpdatedTicket
        fields = ['Resolve']
        widgets = {
            'Resolve': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TicketForm2(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['resolution']
        widgets = {
            'resolution': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Ticket.objects.filter(slug__exact=new_slug).count():
            raise ValidationError('Slug "{}" already exist'.format(new_slug))
        return new_slug