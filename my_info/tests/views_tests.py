#-*- coding:utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from my_info.models import Contact


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
