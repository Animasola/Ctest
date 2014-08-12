#-*- coding:utf-8 -*-
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

import os

from my_info.models import Contact
from my_info.factories import ContactFactory
from my_info.forms import ContactForm


class FormsTestCase(TestCase):

    fixtures = ['initial_data.json']

    def setUp(self):
        self.current_instance = Contact.objects.all()[0]
        self.test_files = []

    def test_form(self):
        # new_form_data = any_model(Co/ntact, birth_date='2014-12-10', photo='')
        new_form_data = ContactFactory.create()
        self.test_files.append(os.path.split(
            settings.DEPLOY_DIR)[0] + new_form_data.photo.url)
        post_dict = new_form_data.__dict__
        form = ContactForm(
            post_dict, instance=self.current_instance)
        self.assertTrue(form.is_valid())
        form.save()

        # data on the main page should be changed now
        response = self.client.get(reverse('home'))
        for key, value in post_dict.iteritems():
            if key == 'birth_date':
                self.assertContains(
                    response,
                    value.strftime('%b. %-d, %Y'),
                    status_code=200)
            elif key in ['extra_contacts', 'bio']:
                self.assertContains(
                    response,
                    value[0],
                    status_code=200)

    def tearDown(self):
        for file_ in self.test_files:
            os.remove(file_)
