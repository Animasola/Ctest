#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
import json

from StringIO import StringIO
from datetime import datetime
from PIL import Image
import os

from my_info.models import Contact, LoggedRequest
from my_info.factories import ContactFactory


class MyInfoViewsTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.my_contacts = Contact.objects.all()[0]
        self.field_names = Contact._meta.get_all_field_names()
        self.test_files = []

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

        chk_priority_request = LoggedRequest.objects.all().order_by('timestamp')[0]
        # check default value of priority is 0
        self.assertEquals(chk_priority_request.priority, 0)

        # two requests should be displayed on page
        self.assertContains(
            get_response,
            reverse('logged_requests_page') + '</td>',
            count=2,
            status_code=200)
        # making 20 requests and making sure
        # only 10 first requests are displayed on page
        for i in xrange(20):
            if i == 19:
                chk_priority_request.priority = 5
                chk_priority_request.save()
                final_response = self.client.get(reverse('logged_requests_page'))
            else:
                self.client.get(reverse('login'))
        # should still be present first two records
        self.assertContains(
            final_response,
            reverse('logged_requests_page') + '</td>',
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
        # check changed priority to the first request
        first_request_in_response = final_response.context['requests'][0]
        self.assertEquals(first_request_in_response.priority, 5)
        self.assertEquals(first_request_in_response, chk_priority_request)

    def test_requests_sorting(self):
        for i in xrange(10):
            self.client.get(reverse('login'))
        first_request = LoggedRequest.objects.all().order_by('timestamp')[0]
        hiest_priority_request = LoggedRequest.objects.all().order_by('timestamp')[1]
        hiest_priority_request.priority = 10
        hiest_priority_request.save()

        # checking timestamp ASC sorting
        url = '%s?ordering=%s' % (reverse('logged_requests_page'), 'timestamp')
        response = self.client.get(url)
        self.assertEquals(
            response.context['requests'][0],
            first_request
        )
        # checking timestamp DESC sorting
        url = '%s?ordering=%s' % (reverse('logged_requests_page'), '-timestamp')
        response = self.client.get(url)
        last_logged_request = LoggedRequest.objects.all().order_by('-timestamp')[0]
        self.assertEquals(
            response.context['requests'][0],
            last_logged_request
        )
        # checking priority ASC sorting
        url = '%s?ordering=%s' % (reverse('logged_requests_page'), 'priority')
        response = self.client.get(url)
        lowest_priority_request = LoggedRequest.objects.all().order_by('priority')[0]
        response = self.client.get(url)
        self.assertEquals(
            response.context['requests'][0],
            lowest_priority_request
        )
        # checking priority DESC sorting
        url = '%s?ordering=%s' % (reverse('logged_requests_page'), '-priority')
        response = self.client.get(url)
        self.assertEquals(
            response.context['requests'][0],
            hiest_priority_request
        )


class ContactsEditPageTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.current_instance = Contact.objects.all()[0]
        self.dummy_file = StringIO()
        self.image = Image.new("RGBA", size=(40, 60), color=(256, 239, 114))
        self.image.save(self.dummy_file, 'png')
        self.dummy_file.name = 'test_%s.png' % datetime.now().microsecond
        self.dummy_file.seek(0)
        self.test_files = []

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

    def test_ajax_request(self):
        expected_redirect = "{0}?next={1}".format(
            reverse('login'), reverse('edit_contacts'))
        # new_form_data = any_model(Contact, birth_date='2014-12-10', photo='')
        new_form_data = ContactFactory.create()
        self.test_files.append(os.path.split(
            settings.DEPLOY_DIR)[0] + new_form_data.photo.url)
        post_dict = new_form_data.__dict__
        del post_dict['photo']
        del post_dict['id']
        post_dict['birth_date'] = str(post_dict['birth_date'].date())
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

    def tearDown(self):
        for file_ in self.test_files:
            os.remove(file_)
