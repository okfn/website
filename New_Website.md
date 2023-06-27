# Plugins

New plugins for blocks of content are located on foundation/okfplugins.

# Creating a new plugin

1. Create a folder on foundation/okfplugins having:

 * admin.py: used on Django Admin interface
 * cms_plugin.py: configuration to appear on the Django CMS content editor sidebar
 * templates/: the django template files (access the plugin variable defined on modesl.py with instance.VARIABLE)
 * models.py: the model for the plugin object on the database

 You can copy a simple plugin as heading or just_text and change the files above. If you do that don't forge to delete the migration files inside migrations/, except by __init__.py.

2. Add the plugin to foundation/settings.py INSTALLED_APPS.

3. Run `python manage.py makemigrations` after you create the models.py.

4. Run the migration to change the database with `python manage.py migrate`

5. Start the server with `python manage.py runserver`

# CSS

To build the css on static/css/styles.css just run `npm run build`. If you use a new tailwind class in some plugin, this class must be added somewhere 
on the file templates/styles.html, otherwise the class will not work when used on the plugin.

The css build is done by vite and the configuration files for it are vite.config.js, tailwind.config.cjs and postcss.config.cjs.

# References for new design and components

 * Components: https://ishigami.github.io/okfn_front/components
 * More components: https://ishigami.github.io/okfn_front/components-2.html
 * Homepage: https://ishigami.github.io/okfn_front/
 * Source: https://github.com/ishigami/okfn_front

