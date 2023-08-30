# !/bin/sh

# Code to clean Plugins or AppHooks.
# python3 manage.py cms uninstall apphooks <AppHook> --noinput
# python3 manage.py cms uninstall plugins <Plugin> --noinput

# This will remove data in cms_cmsplugins table from all non-longer-existing plugins
python3 manage.py cms delete-orphaned-plugins --noinput
