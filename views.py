from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404



@staff_member_required
def index(request):
    """
    Ingenta plugin home page
    :param request: HttpRequest
    :return: HttpResponse
    """

    template = "ingenta/index.html"
    context = {
    }

    return render(request, template, context)

