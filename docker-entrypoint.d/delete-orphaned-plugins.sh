# !/bin/sh

# Given foreign key restrictions, ArticleListItemPlugin we cannot rely on delete-orphaned-plugins
# and we should uninstall it first.
python3 manage.py cms uninstall plugins ArticleListItemPlugin --noinput

# Clean remaining AppHooks left from previous removals.
python3 manage.py cms uninstall apphooks PressReleaseAppHook ThemesAppHook --noinput
python3 manage.py cms uninstall apphooks WorkingGroupsAppHook --noinput

# This will remove data in cms_cmsplugins table from all non-longer-existing plugins
python3 manage.py cms delete-orphaned-plugins --noinput
