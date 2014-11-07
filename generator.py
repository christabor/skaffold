from jinja2 import Environment, PackageLoader
import sys
import json
import os


class JinjaGenerator():
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

    def __init__(self, models, app_name=None):

        # TODO - Finish templates
        #      - Add css / js / static dir
        #      - Integrate rest of django properly so it's
        #           drop-in w/ startproject

        self.app_name = app_name
        self.models = models
        self.templates = {
            'root': '',
            'layouts': '',
            'partials': '',
            'pages': '',
        }

        self.app_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), self.app_name.lower()))
        # Setup template structure
        self.make_app_dirs()
        # Must set custom strings, since we want to keep some of the
        # jinja/django style syntax intact in some outputs (e.g. templates)
        self.env = Environment(
            loader=PackageLoader('_skeleton', ''),
            block_start_string='{%%',
            block_end_string='%%}',
            variable_start_string='{{{',
            variable_end_string='}}}',)
        # Add custom filters to Jinja's context
        self.env.filters['pluralize'] = self.get_plural_inflection
        self.env.filters['singular'] = self.get_singular_inflection

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

    def get_model_field_type(self, prop):
        """Given a prop, returns the closest django model field type."""
        return prop

    def get_modelfactory_field_type(self, prop):
        """Given a prop, returns the closest factory boy field type."""
        return prop

    def get_templates(self, filetype=''):
        return [template for template
                in self.env.list_templates() if template.endswith(filetype)]

    def render_thing(self, thing, **kwargs):
        return self.env.get_template(thing).render(**kwargs)

    def render_admin(self, models=[]):
        return self.render_thing('admin.py', all_models=self.models)

    def render_models(self, models=[]):
        return self.render_thing('models.py', all_models=self.models)

    def render_views(self, models=[]):
        return self.render_thing('views.py', all_models=self.models)

    def render_routes(self, models=[]):
        return self.render_thing(
            'urls.py', app_name=self.app_name, all_models=self.models)

    def render_model_forms(self, models=[]):
        return self.render_thing('forms.py', all_models=self.models)

    def render_model_factories(self, models=[]):
        return self.render_thing('model_factories.py', all_models=self.models)

    def render_tests(self, models=[]):
        """@returns: None"""
        return self.render_thing('tests.py', all_models=self.models)

    def make_app_dirs(self):
        """Creates all necessary directories for a fairly standard
        app structure, and injects paths into self.templates:

            /appname
            /appname/templates
            /appname/templates/layouts
            /appname/templates/pages
            /appname/templates/partials

            @returns: None
        """
        os.mkdir(self.app_root)
        self.templates['root'] = '{}'.format(self.app_root + '/templates')
        self.templates['layouts'] = '{}/layouts'.format(self.templates['root'])
        self.templates['pages'] = '{}/pages'.format(self.templates['root'])
        self.templates['partials'] = '{}/partials'.format(self.templates['root'])

        # Root must exist first.
        os.mkdir(self.templates['root'])
        os.mkdir(self.templates['layouts'])
        os.mkdir(self.templates['pages'])
        os.mkdir(self.templates['partials'])

    def generate_all(self):
        # Always initialize empty list to prevent duplicate data
        self.data = []
        # Create structure for render ouput
        self.data.append({'filename': '__init__.py', 'output': ''})
        self.data.append({'filename': 'views.py', 'output': self.render_views()})
        self.data.append({'filename': 'urls.py', 'output': self.render_routes()})
        self.data.append({'filename': 'admin.py', 'output': self.render_admin()})
        self.data.append({'filename': 'models.py', 'output': self.render_models()})
        self.data.append({'filename': 'forms.py', 'output': self.render_model_forms()})
        self.data.append({'filename': 'model_factories.py', 'output': self.render_model_factories()})
        self.data.append({'filename': 'tests.py', 'output': self.render_tests()})



        # TODO: refactor layouts/pages content, it's used incorrectly atm.



        # Get and render all html templates
        html_templates = self.get_templates(filetype='.html')
        for template in html_templates:
            # Filename relativity (/foo/bar/bim) is maintained
            # from get_templates() so that subdirectories
            # can be mirrored from the _skeleton dir.
            self.data.append({
                'filename': template,
                'output': self.render_thing(
                    template,
                    app_name=self.app_name,
                    all_models=self.models),
            })

        # Save all rendered output as new files for the app
        for rendered in self.data:
            self.save(rendered['output'], rendered['filename'])

    def save(self, rendered, filename):
        with open(self.app_root + '/' + filename, 'w') as newfile:
            newfile.write(rendered + '\n')


def from_cli(app_root, models):
    """A quick util to access the generator from command line"""
    print 'Generating... {}'.format(app_root)
    print '========================'
    gen = JinjaGenerator(models, app_name=app_root)
    gen.generate_all()


if __name__ == '__main__':
    try:
        if not sys.argv[2]:
            print 'No JSON arguments supplied.'
        if sys.argv[1].startswith('--json') and sys.argv[2].endswith('json'):
            json_file = sys.argv[2]
            with open(json_file, 'r') as json_data:
                app_root = raw_input('Enter a folder name for the app root => ')
                fixture_data = dict(json.loads(json_data.read()))
                if not app_root:
                    print 'No folder name was given'
                else:
                    from_cli(app_root, fixture_data['models'])
        else:
            print '`{}` is not a valid .json file'.format(sys.argv[2])
    except IndexError:
        print ('No arguments were specified.'
               ' Please provided a JSON file with'
               ' the `--json filename` parameter.')
