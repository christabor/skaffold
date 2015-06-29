from jinja2 import Environment, PackageLoader
import os
import inflection

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""


class SkaffolderIO:
    """Mixin class for dealing with raw IO aspects of scaffolding.

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

    def _setup_paths(self):
        """Normalizes paths and allows for the use of
        ~ in the self.absolute_path configuration."""
        self.abspath = self.config['absolute_path']
        self.project_name = self.config['project_root']
        self.app_name = self.config['app_name']

        # Setup ~/ if user added to their config.
        if self.abspath.startswith('~'):
            self.abspath = '{}{}'.format(
                os.path.expanduser('~'), self.abspath[1:])

        # Fix slashes in config, if necessary.
        self.project_root = '{}{}'.format(
            self.abspath, self._path_piece(self.project_name))

        self.app_root = '{}{}'.format(
            self.project_root,
            self._path_piece(self.app_name))

    def save(self, rendered, filename, subdirectory=''):
        path = '{}{}{}'.format(self.app_root, subdirectory, filename)
        with open(path, 'w') as newfile:
            newfile.write(rendered + '\n')

    def make_app_dirs(self):
        """Creates all necessary directories for a fairly standard
        app structure, and injects the appropriate paths into self.templates
        Returns:
            None
        """
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
        static_image = self.app_root + '/static/images/'
        static_css = self.app_root + '/static/css/'
        static_js = self.app_root + '/static/js/'

        os.mkdir(static)
        os.mkdir(static_image)
        os.mkdir(static_css)
        os.mkdir(static_js)

        os.mkdir(static_css + 'vendor')
        os.mkdir(static_css + 'app')
        os.mkdir(static_js + 'vendor')
        os.mkdir(static_js + 'app')


class Skaffolder(object, SkaffolderIO):

    def __init__(self, fixtures):
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
        self.env.filters['is_list'] = self.is_list
        self.data = []
        self.fixtures = fixtures
        self.config = self.fixtures['config']
        self.bootstrap = self.config['bootstrap']
        self.templates = {
            'root': '',
            'layouts': '',
            'partials': '',
            'pages': '',
        }
        self.models = self.fixtures['models']
        # Setup all required paths.
        self._setup_paths()

    def _path_piece(self, piece):
        """Always use `path/` style for directory pieces.
        Args:
            piece: the string, representing a directory piece,
                or multple directories; e.g. p1 = `path/to/place/`,
                p2 = 'subdir/path/', ...
        """
        if piece.startswith('/'):
            piece = piece[1:]
        if not piece.endswith('/'):
            piece = piece + '/'
        return piece

    def is_list(self, item):
        return isinstance(item, list)

    def get_singular_inflection(self, word):
        return inflection.singularize(word)

    def get_plural_inflection(self, word):
        """Gets proper plural inflection for a word.
            e.g.
                model: cat, collection: cats
                model: cactus, collection: cacti
        """
        return inflection.pluralize(word)

    def humanize(self, word):
        return inflection.humanize()

    def questionize(self, word):
        """If a user follows the convention of using `is_something`, or
        `has_something`, for a boolean value, the property text will
        automatically be converted into a more human-readable
        format, e.g. 'Something?' for is_ and Has Something? for has_ """
        if word.startswith('is_'):
            return '{}?'.format(word[3:])
        elif word.startswith('has_'):
            return '{}?'.format(word[4:])
        return word

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
