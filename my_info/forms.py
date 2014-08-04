#-*- coding:utf-8 -*-
from django.forms import ModelForm

from my_info.models import Contact
from my_info.widgets import MyDatePicker


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget = MyDatePicker(
            params="dateFormat: 'yy-mm-dd', changeYear: true,"
            " defaultDate: '-16y', yearRange: 'c-40:c+16'",
            attrs={'class': 'datepicker', }
        )

    class Meta:
        model = Contact
