"""
Library for parsing XML metadata files exported from
the Ingenta platform
"""
import datetime
import hashlib

from django.conf import settings


IDENTIFIERS_MAP = {
    "other": "ingenta_id",
    "publisher-id": "pubid",
}


def parse_article_metadata(soup):
    """ Parses article metadata from an Ingenta export
    :param soup: An instance of bs4.BeautifulSoup
    :return: A dict with the parsed metadata
    """
    metadata_soup = soup.find("article-meta")
    meta = {}
    meta["title"] = get_ingenta_title(metadata_soup)
    meta["abstract"] = get_ingenta_abstract(metadata_soup)
    meta["issue"], meta["volume"] = get_ingenta_issue(metadata_soup)
    meta["keywords"] = get_ingenta_keywords(metadata_soup)
    meta["section_name"] = get_ingenta_section(metadata_soup)
    meta["date_published"] = get_ingenta_pub_date(metadata_soup)
    meta["authors"] = []
    meta["date_submitted"] = None
    meta["date_accepted"] = None
    ids = metadata_soup.find_all("article-id")
    for i in ids:
        id_attr = i.attrs.get("pub-id-type")
        id_type = IDENTIFIERS_MAP.get(id_attr, id_attr)
        meta[id_type] = i.text

    authors_soup = metadata_soup.find("contrib-group")
    if authors_soup:
        meta["authors"] = get_ingenta_authors(authors_soup)

    return meta


def get_ingenta_title(soup):
    title = soup.find("article-title")
    if title:
        return title.text
    else:
        return ""


def get_ingenta_abstract(soup):
    abstract = soup.find("abstract")
    if abstract:
        return abstract.text
    else:
        return ""


def get_ingenta_issue(soup):
    issue = soup.find("issue")
    issue = issue.text if issue else 0

    volume = soup.find("volume")
    volume = volume.text if volume else 0

    return (int(issue), int(volume))


def get_ingenta_keywords(soup):
    keywords_soup = soup.find("kwd-group")
    if keywords_soup:
        return {
            keyword.text
            for keyword in keywords_soup.find_all("kwd")
        }
    else:
        return set()


def get_ingenta_section(soup):
    article_element = soup.find("article")
    if article_element:
        return article_element.attrs.get("article-type")
    else:
        return "article"


def get_ingenta_pub_date(soup):
    pub_date_soup = soup.find("pub-date")
    if pub_date_soup:
        day = pub_date_soup.find("day")
        day = day.text if day else 1

        month = pub_date_soup.find("month")
        month = month.text if month else 1

        year = pub_date_soup.find("year").text

        return datetime.date(day=int(day), month=int(month), year=int(year))
    else:
        return None


def get_ingenta_authors(soup):
    authors = []
    for author in soup.find_all("contrib"):
        institution = None
        if author.find("surname"):
            first_name = middle_name = None
            given_names = author.find("given-names")
            if given_names:
                first_name, *middle_names = given_names.text.split(" ")
                middle_name = " ".join(middle_names)
            author_data = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": author.find("surname").text,
                "email": author.find("email") or default_email(author),
                "correspondence": False,
                "institution": institution,
            }
            authors.append(author_data)
    return authors


def default_email(seed):
    hashed = hashlib.md5(str(seed).encode("utf-8")).hexdigest()
    domain = settings.DUMMY_EMAIL_DOMAIN
    if "@" not in domain:
        domain = "@" + domain
    return "{0}{1}".format(hashed, domain)
