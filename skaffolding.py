from jinja2 import Environment, PackageLoader
import os


#   TODO:
#   css/js/images + app/vendor
#   urls for staticpages
#
# Finish templates
#      - Add css / js / static dir
#   proper inflection methods
#   model detail page content.
#
#   notes/readme file output for further user instructions,
#   such as plugging into parent app config
#   docstrings and params


class Skaffolder():
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
        if word.endswith('s'):
            return word[:-1]
        else:
            # Do other inflection stuff.
            return word

    def get_plural_inflection(self, word):
        """Gets proper plural inflection for a word.
            e.g.
                model: cat, collection: cats
                model: cactus, collection: cacti
        """
        # TODO: Add the real deal: http://en.wikipedia.org/wiki/English_plurals
        return word + 's'

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
        app structure, and injects paths into self.templates:

            /appname
            /appname/templates
            /appname/templates/layouts
            /appname/templates/pages
            /appname/templates/partials
            /appname/templates/partials/forms

            @returns: None
        """

        # Root must exist first.
        os.mkdir(self.app_root)
        self.templates['root'] = '{}'.format(self.app_root + '/templates')
        self.templates['layouts'] = '{}/layouts'.format(self.templates['root'])
        self.templates['pages'] = '{}/pages'.format(self.templates['root'])
        self.templates['partials'] = '{}/partials'.format(self.templates['root'])

        # Template root must exist before subdirs.
        os.mkdir(self.templates['root'])
        os.mkdir(self.templates['layouts'])
        os.mkdir(self.templates['pages'])
        os.mkdir(self.templates['partials'])

        # Make other partials folders
        os.mkdir(self.templates['partials'] + '/forms')

        # Make static asset folders.
        os.mkdir(self.app_root + '/images')
        os.mkdir(self.app_root + '/css')
        os.mkdir(self.app_root + '/js')

        os.mkdir(self.app_root + '/css/vendor')
        os.mkdir(self.app_root + '/css/app')
        os.mkdir(self.app_root + '/js/vendor')
        os.mkdir(self.app_root + '/js/app')


class FlaskGenerator(Skaffolder):
    # TODO
    pass


class DjangoGenerator(Skaffolder):

    def __init__(self, fixtures):

        self.data = []
        self.skeleton_root = 'django'
        self.fixtures = fixtures
        self.use_admin = self.fixtures['config']['use_admin']
        self.app_name = self.fixtures['config']['app_name'].lower()
        self.project_root = self.fixtures['config']['project_root'].lower()
        self.models = self.fixtures['models']
        self.templates = {
            'root': '',
            'layouts': '',
            'partials': '',
            'pages': '',
        }

        curr_dir = os.path.dirname(__file__)
        proj_dir = '{}/{}/{}'.format(
            self.project_root, self.project_root, self.app_name)
        self.app_root = os.path.abspath(os.path.join(curr_dir, proj_dir))

        # Setup template structure
        self.make_app_dirs()
        # Must set custom strings, since we want to keep some of the
        # jinja/django style syntax intact in some outputs (e.g. templates)
        self.env = Environment(
            loader=PackageLoader(self.skeleton_root, ''),
            block_start_string='{%%',
            block_end_string='%%}',
            variable_start_string='{{{',
            variable_end_string='}}}',)
        # Add custom filters to Jinja's context
        self.env.filters['pluralize'] = self.get_plural_inflection
        self.env.filters['singular'] = self.get_singular_inflection
        self.env.filters['model_field'] = self.get_model_field_type
        self.env.filters['factory_field'] = self.get_modelfactory_field_type

    def get_model_field_type(self, prop):
        """Given a prop, returns the closest django model field type."""
        if type(prop) == bool:
            return 'models.NullBooleanField()'
        elif type(prop) == int:
            return 'models.IntegerField()'
        elif type(prop) == float:
            return 'models.FloatField()'
        elif type(prop) == str or type(prop) == unicode:
            return 'models.CharField(max_length=50)'

    def get_templates(self, filetype=''):
        return [template for template
                in self.env.list_templates() if template.endswith(filetype)]

    def generate_thing(self, thing, **kwargs):
        return self.env.get_template(thing).render(**kwargs)

    def generate_admin(self):
        return self.generate_thing('admin.py', all_models=self.models)

    def generate_models(self):
        return self.generate_thing('models.py', all_models=self.models)

    def generate_views(self):
        return self.generate_thing(
            'views.py', app_name=self.app_name, all_models=self.models)

    def generate_routes(self):
        return self.generate_thing(
            'urls.py',
            project_root=self.project_root,
            staticpages=self.fixtures['staticpages'],
            use_admin=self.use_admin,
            app_name=self.app_name,
            all_models=self.models)

    def generate_model_forms(self):
        return self.generate_thing('forms.py', all_models=self.models)

    def generate_model_factories(self):
        return self.generate_thing('model_factories.py', all_models=self.models)

    def generate_tests(self):
        return self.generate_thing('tests.py', all_models=self.models)

    def generate_staticpages(self):
        """Allows for static pages to be specified
        and created with the json config"""
        filetype = self.fixtures['staticpages_filetype']
        staticpages = self.fixtures['staticpages']
        for page_title, html_name in staticpages.iteritems():
            output = self.generate_thing(
                'templates/pages/staticpage.html',
                title=page_title)
            self.save(
                output, '{}.{}'.format(html_name, filetype),
                subdirectory='templates/pages/')

    def generate_form_partial(self):
        """Creates all forms from model forms, as reusable blocks
        that can be embedded into any page."""
        self.save(
            self.generate_thing(
                'templates/partials/forms/modelform-generic.html'),
            'modelform-generic.html', subdirectory='templates/partials/forms/')

    def generate_modelpages(self):
        # Get and render all html templates
        html_templates = self.get_templates(filetype='.html')
        for template in html_templates:
            # Filename relativity (/foo/bar/bim) is maintained
            # from get_templates() so that subdirectories
            # can be mirrored from the skeleton_root dir.
            self.data.append({
                'file': template,
                'output': self.generate_thing(
                    template,
                    staticpages=self.fixtures['staticpages'],
                    staticpages_in_nav=self.fixtures['staticpages_in_nav'],
                    project_root=self.project_root,
                    app_name=self.app_name,
                    all_models=self.models),
            })

    def generate_commands(self):
        """Creates new commands for the django application,
        such as fixture generation."""
        os.mkdir(self.app_root + '/management')
        os.mkdir(self.app_root + '/management/commands/')
        # Create init files to make it a proper python module
        self.save('\n', '__init__.py', subdirectory='management/')
        self.save('\n', '__init__.py', subdirectory='management/commands/')
        # Automatically generates a default hook into the model_factories
        # for generating fixture data.
        self.save(
            self.generate_thing(
                'generate_fixtures.py', all_models=self.models),
            'generate_fixtures.py', subdirectory='management/commands/')

    def generate_pyfiles(self):
        """Adds data with each helper method,
        then generates the files in turn."""
        _add = self.data.append
        # Create structure for render ouput
        _add({'file': '__init__.py', 'output': ''})
        _add({'file': 'views.py', 'output': self.generate_views()})
        _add({'file': 'urls.py', 'output': self.generate_routes()})
        _add({'file': 'admin.py', 'output': self.generate_admin()})
        _add({'file': 'models.py', 'output': self.generate_models()})
        _add({'file': 'forms.py', 'output': self.generate_model_forms()})
        _add({'file': 'model_factories.py', 'output': self.generate_model_factories()})
        _add({'file': 'tests.py', 'output': self.generate_tests()})

        # Save all rendered output as new files for the app
        for rendered in self.data:
            self.save(rendered['output'], rendered['file'])

    def generate_all(self):
        """The single source for generating all data at once."""
        # Always initialize empty list to prevent duplicate data
        self.data = []
        # generate primary model/collection pages
        self.generate_modelpages()
        # Save all staticpages
        self.generate_staticpages()
        # Save all html form blocks
        self.generate_form_partial()
        # Generate all django python files
        self.generate_pyfiles()
        # Generate django-admin commands
        self.generate_commands()
