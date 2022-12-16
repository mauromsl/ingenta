import pprint

from django.core.management.base import BaseCommand
from journal import models
from core.models import Account

from plugins.ingenta.importers import import_article


class Command(BaseCommand):
    """ Imports an article from an Ingenta XML metadata file"""

    help = "Imports an article from an Ingenta XML File"

    def add_arguments(self, parser):
        parser.add_argument('xml_path')
        parser.add_argument('journal_code')
        parser.add_argument('--owner_id', default=1)

    def handle(self, *args, **options):
        journal = models.Journal.objects.get(code=options["journal_code"])
        owner = Account.objects.get(pk=options["owner_id"])
        with open(options["xml_path"], "r") as xml_file:
            article = import_article(
                journal, xml_file,
                owner=owner,
            )
