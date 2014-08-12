#-*- coding:utf-8 -*-
from django.test import TestCase
from django.template import Template, Context
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from my_info.models import Contact


class TemplateTagsTestCase(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.current_instance = Contact.objects.all()[0]
        self.admin_url_schema = "admin:{0}_{1}_change"
        self.ct_type = ContentType.objects.get_for_model(
            self.current_instance.__class__)

    def test_admin_edit_tag(self):
        template = Template(
            '{% load admin_edit_link %} {% edit_link object %}'
        )
        context = Context(
            {'object': self.current_instance}
        )

        expected_url = reverse(
            self.admin_url_schema.format(self.ct_type.app_label, self.ct_type.model),
            args=(self.current_instance.id,)
        )
        self.failUnlessEqual(template.render(context).strip(), expected_url)
