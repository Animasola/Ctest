#-*- coding:utf-8 -*-
from django.test import TestCase

from my_info.models import LoggedRequest, ModelChangeLog


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
