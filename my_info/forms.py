#-*- coding:utf-8 -*-
from django.forms import ModelForm

from my_info.models import Contact


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
