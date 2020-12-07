
from django.core.management.base import BaseCommand
from journal import models
from core.models import Account

from plugins.ingenta.importers import import_from_archive


class Command(BaseCommand):
    """ Imports an archive of Ingenta XML and PDF files"""

    help = "Imports an archive of Ingenta XML and PDF files"

    def add_arguments(self, parser):
        parser.add_argument(
            'tarball_path',
            help='Path to the tarball containing the export from Ingenta'
        )
        parser.add_argument('journal_code')
        parser.add_argument('--owner_id', default=1)

    def handle(self, *args, **options):
        journal = models.Journal.objects.get(code=options["journal_code"])
        owner = Account.objects.get(pk=options["owner_id"])
        import_from_archive(options["tarball_path"], journal, owner)
