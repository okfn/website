"""
A simple script to filter the output of the redirects spreadsheet we made into
a CSV suitable for loading into the redirects app with

    python manage.py import_redirects_csv ...

Usage:

    python filter_redirects.py <spreadsheet.csv >redirects.csv

"""

from __future__ import absolute_import, print_function

import csv
import sys

ARCHIVE_ROOT = 'http://webarchive.okfn.org/okfn.org/201404'


def main():
    reader = csv.DictReader(sys.stdin,
                            ['from',
                             'action',
                             'to'])

    # Discard header
    next(reader)

    print('from,to')

    for row in reader:
        if row['action'] == 'keep':
            continue
        elif row['action'] == 'redirect':
            if not row['to'].strip():
                raise RuntimeError('to cannot be blank if action=redirect')
            print('%s,%s' % (_from(row['from']), row['to']))
        elif row['action'] == 'redirect to archive':
            print('%s,%s' % (_from(row['from']), ARCHIVE_ROOT + row['from']))
        elif row['action'] == 'gone':
            print('%s,' % _from(row['from']))
        else:
            raise RuntimeError('unrecognised action: %s' % row['action'])


def _from(url):
    if url.endswith('/'):
        return url
    else:
        return url + '/'


if __name__ == '__main__':
    main()
