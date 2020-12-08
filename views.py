from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404

from identifiers import models as id_models


@staff_member_required
def index(request):
    """
    Ingenta plugin home page
    :param request: HttpRequest
    :return: HttpResponse
    """
    ingenta_ids = id_models.Identifier.objects.filter(
        id_type="ingenta_id",
    ).select_related(
        "article",
    )
    if request.journal:
        ingenta_ids.filter(article__journal=request.journal)
    ingenta_ids.order_by("-article__date_published")

    template = "ingenta/index.html"
    context = {
        "ingenta_ids": ingenta_ids,
    }

    return render(request, template, context)
