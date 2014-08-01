#-*- coding:utf-8 -*-
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Name")
    last_name = models.CharField(max_length=75, verbose_name="Last Name")
    birth_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name="Date Of Birth")
    bio = models.TextField(verbose_name="Short Biography")
    email = models.EmailField(max_length=75, verbose_name="Email Address")
    jabber = models.CharField(max_length=50)
    skype = models.CharField(max_length=50)
    extra_contacts = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.last_name, self.first_name)


class LoggedRequest(models.Model):
    url = models.CharField(max_length=255)
    ip = models.CharField(max_length=20)
    request_type = models.CharField(max_length=4)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return "Request: %s From: %s At: %s" % (
            self.request_type, self.ip, self.timestamp)
