import csv
import errno
from optparse import make_option
import sys

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Import redirects from a CSV"
    args = "<file>"

    option_list = BaseCommand.option_list + (
        make_option('--site',
                    dest="site",
                    default=Site.objects.get_current(),
                    help=("The domain of the site to import redirects into. "
                          "(Defaults to current site.)")),
    )

    def execute(self, *args, **options):
        if len(args) != 1:
            raise CommandError("You must provide a file to import!")

        self.site = options["site"]
        if not isinstance(self.site, Site):
            try:
                self.site = Site.objects.get(domain=options["site"])
            except ObjectDoesNotExist:
                raise CommandError("No site found for domain: %s"
                                   % options["site"])

        filepath = args[0]

        if filepath == '-':
            rows = _get_rows(sys.stdin)
            _create_redirects(self.site, rows)
        else:
            try:
                with open(filepath) as fp:
                    rows = _get_rows(fp)
                    _create_redirects(self.site, rows)

            except IOError as e:
                if e.errno == errno.ENOENT:
                    raise CommandError("The specified file does not exist!")
                else:
                    raise


def _get_rows(fp):
    reader = csv.reader(fp)

    header = reader.next()
    if sorted(header) != ["from", "to"]:
        raise CommandError("CSV should have 'from' and 'to' columns!")

    return csv.DictReader(fp, header)


def _create_redirects(site, rows):
    for row in rows:
        old_path = row["from"]
        new_path = row["to"]
        redirect = Redirect(site=site, old_path=old_path, new_path=new_path)
        redirect.save()
