#-*- coding:utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe


class MyDatePicker(forms.DateInput):

    def __init__(self, params='', attrs=None):
        self.params = params
        super(MyDatePicker, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(MyDatePicker, self).render(name, value, attrs=attrs)

        return rendered + mark_safe(
            ''' <script type="text/javascript">\
                    $('#id_%s').datepicker({%s});
                </script>''' % (name, self.params, ))
