Skaffold - auto scaffolding for your MVC web applications!
============================================================

# How does it work?

By using the wonderful [Jinja2 templating engine](https://github.com/mitsuhiko/jinja2), the output of a standard python web application is rendered via *JSON config*. There is also support for inflection, and it provides a few extra features out of the box:

* Model factories via [Factory Boy](https://github.com/rbarrois/factory_boy)
* Test definitions with standard CRUD testing and input testing.
* Models, Views Controllers and Routers
* Templating:
    * Any arbitrary static page
    * Form partials for CRUD operations
    * Model and Collection views
* (Django) custom commands for fixture generation `python manage.py generate_fixtures`
* Typical app structure:
    * CSS, JS and image folder, with app/vendor subfolders.
* Bootstrap-3 styling/integration.
* [Django bootstrap-3](https://github.com/dyve/django-bootstrap3) integration.

## Who is it for?

Skaffold is simple and opinionated. It provides very vanilla layout options, so it's meant for those who either:

1. Want the boilerplate setup complete, to style and improve upon.
2. Non web-app developers who want an app up and running quickly.
3. Mechanization of any sort, for auto-generating applications.

## Dependencies

### All
* inflection
* jinja

### Django
* django-bootstrap
* factory boy

## Current support

#### Django

Currently implemented.

#### Flask

TBD

## JSON Config options:

**See example.json for details and best examples.**

* upload_to (str) - the path *beyond what is already defined in settings file*. Must end in trailing slash. (Django)
* project_root (str) - the name of your primary application parent project (required for Django)
* app_name (str) - the name of your individual application
* use_admin (bool) - whether or not to use admin (Django)

* staticpages_in_nav (bool) - whether or not to render the staticpage links in the primary navigation

### Model Config

* display_as: display_type (str) - how to show a given collection of models on the list (collection) page. Options such as table, list, or panel (boostrap 3) are supported, with perhaps more to come.
* classes: class list (array) - a list of classes to apply to the html representation
* data_attrs: attrs list (array) - a list of data attributes to apply to the html representation

#### Specifying property types

Types are inferred by default, buy a few must be specified. To avoid making configuration extra work, simple "flags" are specified in place of the equivalent, verbose property:
* \__M2M__: specifes the Many2Many relationship, with the model (e.g. "model": "\__M2M__") (Django)
* \__FILE__: specifies that the property should be a FileField (Django)

### Static assets
**CSS/JSS**
* active: (boolean) - if custom css should be shown in base template
* libs: (array) - a list of names of libraries to add

### Staticpages:
* title: filename (str) - a key/value list of static pages, with k = title, v = filename

* static_pages_filetype (str) - the filetype to use for static pages (e.g html, hbs, templ, etc...)

### Models:
* modelname, properties (obj) - a model name, with child key/value pairs for each model property and value.

### TODO:
* More support beyond django (Flask, etc...)

