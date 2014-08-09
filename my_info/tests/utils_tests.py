#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import Template, Context
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType

from StringIO import StringIO

from my_info.models import Contact, LoggedRequest, ModelChangeLog


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


class SignalModelLoggerTestCase(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        # creating object
        self.request = LoggedRequest.objects.create()

    def test_creation(self):
        log_record = ModelChangeLog.objects.all().order_by('-timestamp')[0]
        self.assertEquals(
            log_record.model_name, self.request.__class__.__name__)
        self.assertEquals(log_record.app_label, self.request._meta.app_label)
        self.assertEquals(log_record.action, ModelChangeLog.CREATED)

    def test_alter_delete(self):
        # change url field
        self.request.url = 'google.com.ua'
        self.request.save()
        log_record = ModelChangeLog.objects.all().order_by('-timestamp')[0]
        self.assertEquals(
            log_record.model_name, self.request.__class__.__name__)
        self.assertEquals(log_record.app_label, self.request._meta.app_label)
        self.assertEquals(log_record.action, ModelChangeLog.ALTERED)
        # delete record
        self.request.delete()
        log_record = ModelChangeLog.objects.all().order_by('-timestamp')[0]
        self.assertEquals(
            log_record.model_name, self.request.__class__.__name__)
        self.assertEquals(log_record.app_label, self.request._meta.app_label)
        self.assertEquals(log_record.action, ModelChangeLog.DELETED)
