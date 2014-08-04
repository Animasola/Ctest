#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json

from StringIO import StringIO
from datetime import datetime

from PIL import Image
from django_any import any_model

from my_info.models import Contact, LoggedRequest
from my_info.forms import ContactForm


class MyInfoViewsTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.my_contacts = Contact.objects.all()[0]
        self.field_names = Contact._meta.get_all_field_names()

    def test_page_content(self):

        response = self.client.get(reverse('home'))
        # all field values except "id" should be present at the home page
        for field_name in [field for field in self.field_names if field != 'id']:
            if field_name == 'birth_date':
                self.assertContains(
                    response,
                    self.my_contacts.birth_date.strftime('%B %d, %Y'),
                    status_code=200)
            else:
                self.assertContains(
                    response,
                    getattr(self.my_contacts, field_name),
                    status_code=200)

    def test_request_logger(self):
        # shouldn't be any logged requests yet
        logged_requests = LoggedRequest.objects.all()
        self.assertEquals(logged_requests.count(), 0)
        # only GET requests allowed
        post_response = self.client.post(reverse('logged_requests_page'))
        self.assertEquals(post_response.status_code, 405)
        get_response = self.client.get(reverse('logged_requests_page'))
        self.assertEquals(get_response.status_code, 200)
        # should be 2 requests in db
        logged_requests = LoggedRequest.objects.all()
        self.assertEquals(logged_requests.count(), 2)
        # two requests should be displayed on page
        self.assertContains(
            get_response,
            reverse('logged_requests_page'),
            count=2,
            status_code=200)
        # making 20 requests and making sure
        # only 10 first requests are displayed on page
        for i in xrange(20):
            if i == 19:
                final_response = self.client.get(reverse('logged_requests_page'))
            else:
                self.client.get(reverse('login'))
        # should still be present first two records
        self.assertContains(
            final_response,
            reverse('logged_requests_page'),
            count=2,
            status_code=200)
        # should be only 8 requests to login page displayed
        self.assertContains(
            final_response,
            reverse('login'),
            count=8,
            status_code=200)
        # total logged requests count in db should equal to 22
        self.assertEquals(
            LoggedRequest.objects.all().count(),
            22)


class ContactsEditPageTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.current_instance = Contact.objects.all()[0]
        self.dummy_file = StringIO()
        self.image = Image.new("RGBA", size=(40, 60), color=(256, 239, 114))
        self.image.save(self.dummy_file, 'png')
        self.dummy_file.name = 'test_%s.png' % datetime.now().microsecond
        self.dummy_file.seek(0)
        # self.form_data = any_model(Contact, photo="")
        # self.post_data = self.form_data.__dict__

    def test_get(self):
        # need to be authenticated
        response = self.client.get(reverse('edit_contacts'))
        self.assertEquals(response.status_code, 302)

        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('edit_contacts'))
        self.assertEquals(response.status_code, 200)
        # should only one instance in Contact model
        self.assertEquals(
            Contact.objects.all().count(), 1)
        # checking each field's data is present in response
        for field_name, value in self.current_instance.__dict__.iteritems():
            if field_name in ['_state', 'id']:
                continue
            self.assertContains(response, value, status_code=200)

    def test_form(self):
        new_form_data = any_model(Contact, birth_date='2014-12-10', photo='')
        post_dict = new_form_data.__dict__
        file_dict = {
            'photo': SimpleUploadedFile(self.dummy_file.name, self.dummy_file.read())
        }
        form = ContactForm(
            post_dict, file_dict, instance=self.current_instance)
        self.assertTrue(form.is_valid())
        form.save()

        # data on the main page should be changed now
        response = self.client.get(reverse('home'))
        for key, value in post_dict.iteritems():
            if key == 'birth_date':
                self.assertContains(
                    response,
                    value.strftime('%b. %d, %Y'),
                    status_code=200)
            elif key in ['extra_contacts', 'bio']:
                self.assertContains(
                    response,
                    value[0],
                    status_code=200)

    def test_ajax_request(self):
        expected_redirect = "{0}?next={1}".format(
            reverse('login'), reverse('edit_contacts'))
        new_form_data = any_model(Contact, birth_date='2014-12-10', photo='')
        post_dict = new_form_data.__dict__
        del post_dict['photo']
        del post_dict['id']
        # need to be authenticated
        response = self.client.post(
            reverse('edit_contacts'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertRedirects(
            response,
            expected_redirect,
            status_code=302,
            target_status_code=200,
            msg_prefix=''
        )

        self.client.login(username='admin', password='admin')
        # with no submitted data
        response = self.client.post(
            reverse('edit_contacts'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn('application/json', response['Content-Type'])
        data = json.loads(response.content)
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('result' in data)
        self.assertEquals(data['result'], 'error')
        self.assertTrue('form_errors' in data)
        # with data
        response = self.client.post(
            reverse('edit_contacts'),
            post_dict,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('result' in data)
        self.assertEquals('success', data['result'])
