import os
from inflection import pluralize
from inflection import singularize

#   TODO:
#   css/js/images + app/vendor
#
# Finish templates
#      - Add css / js / static dir
#   proper inflection methods
#   model detail page content.
#   docstrings and params


class Skaffolder:
    """
    = route (urls)
        view model
        view collection
        delete model
        update model
        add model

    = views
        view collection
        view detail

    = models
        model

    = forms
        modelform

    = factory
        modelfactory

    = test
        edit all fields
        delete model
        add model

    = templates
        view collection
        view detail
        edit collection
        index (home)

        = partials
            success message
            collection-list
                collection-list-item
            form-edit-{{ model_name }}
            header
                navigation
    """

    def save(self, rendered, filename, subdirectory=''):
        with open('{}/{}{}'.format(
                self.app_root, subdirectory, filename), 'w') as newfile:
            newfile.write(rendered + '\n')

    def get_singular_inflection(self, word):
        return singularize(word)

    def get_plural_inflection(self, word):
        """Gets proper plural inflection for a word.
            e.g.
                model: cat, collection: cats
                model: cactus, collection: cacti
        """
        return pluralize(word)

    def get_modelfactory_field_type(self, prop):
        """Given a prop, returns the closest factory boy field type."""
        if type(prop) == bool:
            return 'fuzzy.FuzzyChoice([True, False])'
        elif type(prop) == int:
            return 'fuzzy.FuzzyInteger(0, 99)'
        elif type(prop) == float:
            return 'fuzzy.FuzzyFloat(0.1, 1.0)'
        elif type(prop) == str or type(prop) == unicode:
            return 'fuzzy.FuzzyText(length=10)'
        return prop

    def make_app_dirs(self):
        """Creates all necessary directories for a fairly standard
        app structure, and injects the appropriate paths into self.templates
        Returns:
            None
        """

        # Root must exist first.
        os.mkdir(self.app_root)
        self.templates['root'] = '{}'.format(self.app_root + '/templates')
        self.templates['layouts'] = '{}/layouts'.format(self.templates['root'])
        self.templates['pages'] = '{}/pages'.format(self.templates['root'])
        self.templates['partials'] = '{}/partials'.format(
            self.templates['root'])

        # Template root must exist before subdirs.
        os.mkdir(self.templates['root'])
        os.mkdir(self.templates['layouts'])
        os.mkdir(self.templates['pages'])
        os.mkdir(self.templates['partials'])

        # Make other partials folders
        os.mkdir(self.templates['partials'] + '/forms')
        os.mkdir(self.templates['partials'] + '/models')

        # Make static asset folders.
        static = self.app_root + '/static/'
        static_image = self.app_root + '/static/js/'
        static_css = self.app_root + '/static/images/'
        static_js = self.app_root + '/static/css/'

        os.mkdir(static)
        os.mkdir(static_image)
        os.mkdir(static_css)
        os.mkdir(static_js)

        os.mkdir(static_css + '/vendor')
        os.mkdir(static_css + 'app')
        os.mkdir(static_js + 'vendor')
        os.mkdir(static_js + 'app')
