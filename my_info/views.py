#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from my_info.models import Contact, LoggedRequest
from my_info.forms import ContactForm


@require_GET
@render_to('my_info/home.html')
def info_page(request):
    my_contacts = get_object_or_404(Contact, pk=1)
    return {'contacts': my_contacts}


@require_GET
@render_to('my_info/requests.html')
def logged_requests_page(request):
    requests = LoggedRequest.objects.all().order_by('timestamp')[: 10]
    return {'requests': requests}


@login_required
@render_to('my_info/edit_contacts.html')
def edit_contacts(request):
    my_contacts = get_object_or_None(Contact, id=1)

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=my_contacts)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
    else:
        form = ContactForm(instance=my_contacts)

    return {'form': form, 'photo': my_contacts.photo}
