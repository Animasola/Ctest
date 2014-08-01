#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from my_info.models import Contact, LoggedRequest


class MyInfoViewsTests(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.my_contacts = Contact.objects.all()[0]
        self.field_names = Contact._meta.get_all_field_names()

    def test_page_content(self):
        # should be asking to login
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='admin', password='admin')
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
