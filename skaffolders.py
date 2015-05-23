from jinja2 import Environment, PackageLoader
import os
from skaffolder import Skaffolder


class FlaskSkaffolder(Skaffolder):
    # TODO
    pass


class DjangoSkaffolder(Skaffolder):

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
            trim_blocks=True,
            lstrip_blocks=True,
            block_start_string='{%%',
            block_end_string='%%}',
            variable_start_string='{{{',
            variable_end_string='}}}',)
        # Add custom filters to Jinja's context
        self.env.filters['pluralize'] = self.get_plural_inflection
        self.env.filters['singularize'] = self.get_singular_inflection
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
            return 'models.CharField(blank=True, max_length=50)'

    def get_templates(self, filetype='.html'):
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
            'views.py',
            app_name=self.app_name,
            all_models=self.models,
            model_config=self.fixtures['model_config'])

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

    def generate_form_partials(self):
        """Creates all forms from model forms, as reusable blocks
        that can be embedded into any page."""
        self.save(
            self.generate_thing(
                'templates/partials/forms/modelform-generic.html'),
            'modelform-generic.html', subdirectory='templates/partials/forms/')

    def generate_layouts(self):
        html_templates = self.get_templates()
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
                    css_config=self.fixtures['static_config']['css_config'],
                    js_config=self.fixtures['static_config']['js_config'],
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
                'generate_fixtures.py',
                all_models=self.models, project=self.project_root,
                app_name=self.app_name),
            'generate_fixtures.py', subdirectory='management/commands/')

    def generate_pyfiles(self):
        """Adds data with each helper method,
        then generates the files in turn."""
        _add = self.data.append
        # Create structure for render ouput
        to_generate = [
            ['__init__.py', ''],
            ['views.py', self.generate_views],
            ['urls.py', self.generate_routes],
            ['admin.py', self.generate_admin],
            ['models.py', self.generate_models],
            ['forms.py', self.generate_model_forms],
            ['model_factories.py', self.generate_model_factories],
            ['tests.py', self.generate_tests],
        ]
        for item in to_generate:
            filename, output = item
            output = output() if hasattr(output, '__call__') else output
            _add({'file': filename, 'output': output})

        # Save all rendered output as new files for the app
        for rendered in self.data:
            self.save(rendered['output'], rendered['file'])

    def generate_all(self):
        """The single source for generating all data at once."""
        # Always initialize empty list to prevent duplicate data
        self.data = []
        self.generate_layouts()
        self.generate_staticpages()
        self.generate_form_partials()
        self.generate_pyfiles()
        # Generate django-admin commands
        self.generate_commands()
