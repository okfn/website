# !/bin/sh

# Clean remaining AppHooks left from previous removals.
# python3 manage.py cms uninstall apphooks <AppHook> --noinput


# This will remove data in cms_cmsplugins table from all non-longer-existing plugins
python3 manage.py cms delete-orphaned-plugins --noinput
