#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from annoying.decorators import render_to
from my_info.models import Contact, LoggedRequest


@require_GET
@login_required
@render_to('my_info/home.html')
def info_page(request):
    my_contacts = get_object_or_404(Contact, pk=1)
    return {'contacts': my_contacts}


@require_GET
@render_to('my_info/requests.html')
def logged_requests_page(request):
    requests = LoggedRequest.objects.all().order_by('timestamp')[: 10]
    return {'requests': requests}
