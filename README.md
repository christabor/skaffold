Skaffold - auto scaffolding for your python web applications!
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
* Typical app structure:
    * CSS, JS and image folder, with app/vendor subfolders.
* Bootstrap-3 styling/integration.
* [Django bootstrap-3](https://github.com/dyve/django-bootstrap3) integration.

## Who is it for?

Skaffold is simple and opinionated. It provides very vanilla layout options, so it's meant for those who either:

1. Want the boilerplate setup complete, to style and improve upon.
2. Non web-app developers who want an app up and running quickly.
3. Mechanization of any sort, for auto-generating applications.

### Current support

#### Django

Currently implemented.

#### Flask

TBD

## JSON options
