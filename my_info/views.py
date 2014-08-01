#-*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to
from my_info.models import Contact


@login_required
@render_to('my_info/home.html')
def info_page(request):
    my_contacts = get_object_or_404(Contact, pk=1)
    return {'contacts': my_contacts}
