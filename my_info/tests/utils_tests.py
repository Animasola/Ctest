#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType

from StringIO import StringIO


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


class CommandsTestCase(TestCase):

    fixtures = ['initial_data.json']

    def test_all_models_command(self):
        stdout = StringIO()
        stderr = StringIO()
        call_command('models_info', stderr=stderr, stdout=stdout)
        for out, err in zip(stdout.readlines(), stderr.readlines()):
            self.assertEquals(err, 'Error: %s' % out)
        for model in ContentType.objects.all():
            self.assertIn('%s: %s - %s' % (
                model.app_label,
                model.model,
                model.model_class().objects.count()),
                stdout.getvalue()
            )
