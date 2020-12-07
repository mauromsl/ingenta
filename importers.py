from bs4 import BeautifulSoup
from django.db import transaction
from django.conf import settings

from core.models import Account
from identifiers.models import Identifier
from submission import models as submission_models

from plugins.ingenta import parsers


def import_journal():
    pass


def import_issue():
    pass


def import_article(journal, xml_file, owner, article_pdf=None):

    xml_contents = xml_file.read()
    article = import_article_xml(journal, xml_contents, owner)
    if article_pdf and not article.pdfs:
        pass  # TODO


def import_article_xml(journal, xml_contents, owner):
    soup = BeautifulSoup(xml_contents, 'lxml')
    metadata = parsers.parse_article_metadata(soup)
    article = get_or_create_article(journal, metadata, owner)


def get_or_create_article(journal, metadata, owner):
    with transaction.atomic():
        article = None
        section, _ = submission_models.Section.objects \
            .language(settings.LANGUAGE_CODE).get_or_create(
                journal=journal,
                name=metadata["section_name"],
        )
        for id_type in {"doi", "ingenta_id", "sici"}:
            if metadata.get(id_type):
                try:
                    ident = Identifier.objects.get(
                        id_type=id_type, identifier=metadata[id_type])
                except Identifier.DoesNotExist:
                    continue
                else:
                    article = ident.article
                    break

        if not article:
            article = submission_models.Article.objects.create(
                journal=journal,
                title=metadata["title"],
                abstract=metadata["abstract"],
                date_published=metadata["date_published"],
                date_accepted=metadata["date_accepted"],
                date_submitted=metadata["date_submitted"],
                stage=submission_models.STAGE_PUBLISHED,
                is_import=True,
                owner=owner,
            )
        import_article_authors(article, metadata)

        for id_type in {"doi", "ingenta_id", "sici"}:
            if metadata.get(id_type):
                Identifier.objects.get_or_create(
                    id_type=id_type,
                    identifier=metadata[id_type],
                    article=article,
                )

        return article


def import_article_authors(article, metadata):
    authors = metadata["authors"]
    for author in authors:
        account, _ = Account.objects.get_or_create(
            email=author["email"],
            defaults={
                "first_name": author["first_name"],
                "middle_name": author["middle_name"],
                "last_name": author["last_name"],
                # Ingenta only provides author names
                "institution": article.journal.name,
            }
        )
        article.authors.add(account)
    article.snapshot_authors(article)


