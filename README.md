# Ingenta Plugin for Janeway.
This is a plugin for ingesting back content from the Ingenta platform into Janeway
It requires an SGML dump from the publication to be migrated.

## Installation instructions
Clone this repository under `/path/to/janeway/src/plugins` and run the `install_plugins` command
More information about the Janeway plugin framework is available here: https://github.com/BirkbeckCTP/janeway/wiki/Plugin-Framework

## Usage
This plugin supports two import mechanisms as django commands:
- Import a collection of articles from a a tarball (`import_ingenta_dump`)
```
usage: manage.py import_ingenta_dump [-h] [--version] [-v {0,1,2,3}]                                                                                                                                                                                  [--settings SETTINGS]                                                                                                                                                                                            [--pythonpath PYTHONPATH] [--traceback]                                                                                                                                                                          [--no-color] [--owner_id OWNER_ID]                                                                                                                                                                               tarball_path journal_code

Imports an archive of Ingenta XML and PDF files

positional arguments:
  tarball_path          Path to the tarball containing the export from Ingenta                                                                                                                                     journal_code

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}                                                                                                                                                                                                    Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --owner_id OWNER_ID
root@1cddc7ffcf40:/vol/janeway# python src/manage.py import_ingenta_article --help                                                                                                                               usage: manage.py import_ingenta_article [-h] [--version] [-v {0,1,2,3}]
                                        [--settings SETTINGS]
                                        [--pythonpath PYTHONPATH]
                                        [--traceback] [--no-color]
                                        [--owner_id OWNER_ID]
                                        xml_path journal_code
```

- Import a single article from an article's SGML metadata (`import_ingenta_article`)
```
usage: manage.py import_ingenta_article [-h] [--version] [-v {0,1,2,3}]
                                        [--settings SETTINGS]
                                        [--pythonpath PYTHONPATH]
                                        [--traceback] [--no-color]
                                        [--owner_id OWNER_ID]
                                        xml_path journal_code

Imports an article from an Ingenta XML File

positional arguments:
  xml_path
  journal_code

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --owner_id OWNER_ID
```

## Imported metadata:
The plugin will import the following metadata and files:
- Basic article metadata (title, abstract, section, keywords)
- Issue/volume structure
- Author names (no other author metadata is provided by Ingenta SGML schema)
- Date published
- PDF article files
- Identifiers: DOI, SICI, Ingenta ID, public ID

## Notes
When an article import is requested for an article that had been previously processed (matched by ingenta ID), no duplicates will be created.
Instead, the plugin will update the article metadata as well as load in any missing files.
