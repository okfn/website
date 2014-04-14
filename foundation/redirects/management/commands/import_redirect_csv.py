import csv
import errno
from optparse import make_option

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
        filepath = args[0]

        try:
            with open(filepath) as fp:
                reader = csv.reader(fp)
                header = reader.next()
                if sorted(header) != ["from", "to"]:
                    raise CommandError("File should have 'from' and 'to' "
                                       "columns!")

                dictreader = csv.DictReader(fp, header)

                site = options["site"]
                if not isinstance(site, Site):
                    try:
                        site = Site.objects.get(domain=options["site"])
                    except ObjectDoesNotExist:
                        raise CommandError("No site found for domain: %s"
                                           % options["site"])

                _create_redirects(site, dictreader)

        except IOError as e:
            if e.errno == errno.ENOENT:
                raise CommandError("The specified file does not exist!")
            else:
                raise


def _create_redirects(site, rows):
    for row in rows:
        old_path = row["from"]
        new_path = row["to"]
        redirect = Redirect(site=site, old_path=old_path, new_path=new_path)
        redirect.save()
