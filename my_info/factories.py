import factory
from datetime import datetime

from my_info.models import Contact


class ContactFactory(factory.Factory):

    FACTORY_FOR = Contact

    first_name = 'Sunny'
    last_name = 'Bunny'
    birth_date = datetime.now()
    bio = "Sunny Bunny Booring Biography"
    email = 'sunny@mail.com'
    jabber = 'sunny@jabber.com'
    skype = 'sunny_bunny'
    extra_contacts = "mob. 0998877654"
    photo = factory.django.ImageField(color='blue')
