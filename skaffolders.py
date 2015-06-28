import os
from skaffolder import Skaffolder


class DjangoSkaffolder(Skaffolder):

    def __init__(self, fixtures):
        # Template directory for jinja, required before all else
        self.skeleton_root = 'django'
        # Base setup
        super(DjangoSkaffolder, self).__init__(fixtures)
        # Customer django settings
        self.use_admin = self.config['use_admin']
        self.upload_dir = self.config['upload_dir']
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
        kwargs.update({'config': self.config})
        return self.env.get_template(thing).render(**kwargs)

    def generate_admin(self):
        return self.generate_thing('admin.py', all_models=self.models)

    def generate_models(self):
        return self.generate_thing(
            'models.py', upload_dir=self.upload_dir, all_models=self.models)

    def generate_views(self):
        return self.generate_thing(
            'views.py',
            project_root=self.project_name,
            app_name=self.app_name,
            all_models=self.models,
            model_config=self.fixtures['model_config'])

    def generate_routes(self):
        return self.generate_thing(
            'urls.py',
            project_root=self.project_name,
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
                'templates/pages/staticpage.html', title=page_title)
            self.save(output, '{}.{}'.format(html_name, filetype),
                      subdirectory='templates/pages/')

    def generate_form_partials(self):
        """Creates all forms from model forms, as reusable blocks
        that can be embedded into any page."""
        return self.save(
            self.generate_thing(
                'templates/partials/forms/modelform-generic.html',
                bootstrap_config=self.config['bootstrap']),
            'modelform-generic.html', subdirectory='templates/partials/forms/')

    def generate_layouts(self):
        html_templates = self.get_templates()
        bootstrap_config = self.config['bootstrap']
        for template in html_templates:
            # Filename relativity (/foo/bar/bim) is maintained
            # from `get_templates()` so that subdirectories
            # can be mirrored from the `skeleton_root` dir.
            self.data.append({
                'file': template,
                'output': self.generate_thing(
                    template,
                    bootstrap_config=bootstrap_config,
                    staticpages=self.fixtures['staticpages'],
                    staticpages_in_nav=self.fixtures['staticpages_in_nav'],
                    css_config=self.fixtures['static_config']['css_config'],
                    js_config=self.fixtures['static_config']['js_config'],
                    project_root=self.project_name,
                    app_name=self.app_name,
                    all_models=self.models),
            })

    def generate_commands(self):
        """Creates new commands for the django application,
        such as fixture generation."""
        os.mkdir(self.app_root + 'management')
        os.mkdir(self.app_root + 'management/commands/')
        # Create init files to make it a proper python module
        self.save('\n', '__init__.py', subdirectory='management/')
        self.save('\n', '__init__.py', subdirectory='management/commands/')
        # Automatically generates a default hook into the model_factories
        # for generating fixture data.
        self.save(
            self.generate_thing(
                'generate_fixtures.py',
                all_models=self.models, project=self.app_name,
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
        print('[SKAFFOLD] Generating layouts')
        self.generate_layouts()
        print('[SKAFFOLD] Generating staticpages')
        self.generate_staticpages()
        print('[SKAFFOLD] Generating partials')
        self.generate_form_partials()
        print('[SKAFFOLD] Generating python files')
        self.generate_pyfiles()
        # Generate django-admin commands
        print('[SKAFFOLD] Generating django commands')
        self.generate_commands()
