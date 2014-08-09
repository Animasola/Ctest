#-*- coding:utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from annoying.decorators import render_to
from annoying.functions import get_object_or_None
import json

from my_info.models import Contact, LoggedRequest
from my_info.forms import ContactForm


SORTING = {
    'timestamp': "Timestamp ASC",
    '-timestamp': "Timestamp DESC",
    'priority': "Priority ASC",
    '-priority': "Priority DESC"
}


@require_GET
@render_to('my_info/home.html')
def info_page(request):
    my_contacts = get_object_or_404(Contact, pk=1)
    return {'contacts': my_contacts}


@require_GET
@render_to('my_info/requests.html')
def logged_requests_page(request):

    queryset = LoggedRequest.objects.all()
    ordering = 'timestamp'

    if 'ordering' in request.GET and request.GET['ordering']:
        ordering = request.GET['ordering']
    requests = queryset.order_by(ordering)[: 10]

    return {'requests': requests, 'sorting': SORTING, 'active': ordering}


@login_required
@render_to('my_info/edit_contacts.html')
def edit_contacts(request):
    my_contacts = get_object_or_None(Contact, id=1)

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=my_contacts)
        response_dict = {}
        if request.is_ajax():
            if form.is_valid():
                form.save()
                response_dict['result'] = 'success'
            else:
                response_dict['result'] = 'error'
                errors = {}
                for error in form.errors:
                    errors[error] = form.errors[error][0]
                response_dict['form_errors'] = errors
            data = json.dumps(response_dict, ensure_ascii=False)
            return HttpResponse(data, mimetype='application/json')
        else:
            if form.is_valid():
                form.save()
                return redirect(reverse('home'))
    else:
        form = ContactForm(instance=my_contacts)

    return {'form': form, 'photo': my_contacts.photo}
