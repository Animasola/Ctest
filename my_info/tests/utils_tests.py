#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings


class ContextProcessorTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_settings_in_template_context(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('home'))
        self.assertTrue('django_settings' in response.context)
        django_settings = response.context['django_settings']

        for i in dir(settings):
            self.assertEquals(
                getattr(settings, i),
                getattr(django_settings, i)
            )
