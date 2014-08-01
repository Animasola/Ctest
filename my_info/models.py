#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals


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


# for getBarista
def create_superuser(app, created_models, verbosity, **kwargs):
    if User.objects.all().count() == 0:
        User.objects.create_superuser("admin", "admin@mail.com", "admin")

signals.post_syncdb.connect(create_superuser, dispatch_uid='create_superuser')
