"""
The djangocms_betterpageurl app is a custom hack to enable a better
``page_url`` tag for django-cms. The current tag raises an exception if the
referenced page cannot be found, forcing a coupling between content in the
database and templates. This is ugly, and one proposed solution is to give the
``page_url`` tag an optional "as varname" parameter, allowing template authors
to control what happens if the page is not found in the database with code
like the following:

    {% load better_page_url_tags %}
    ...
    {% page_url "foo" as foo_url %}
    {% if foo_url %}{{ foo_url }}{% else %}http://default/url{% endif %}

For further details, see https://github.com/divio/django-cms/issues/1479.
"""
