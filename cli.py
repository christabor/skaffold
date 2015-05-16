import os
import sys
import json
from skaffolders import FlaskSkaffolder
from skaffolders import DjangoSkaffolder

generators = {
    'django': DjangoSkaffolder,
    'flask': FlaskSkaffolder,
}


def _clean(root_dir):
    print('Deleting existing project (if applicable) located at {}'.format(
        root_dir))
    os.system('rm -r ' + root_dir)


def from_scratch_django(fixture_data):
    """Does all work required to setup a completely new application."""
    project_name = fixture_data['config']['project_root']
    app_name = fixture_data['config']['app_name']
    root_dir = os.getcwd() + '/' + project_name + '/'
    settings_file = root_dir + '/' + project_name + '/settings.py'

    _clean(root_dir)

    print('Adding new django project...')
    os.system('django-admin.py startproject ' + project_name)

    print('Skaffolding app structure...')
    new_app_django(fixture_data)

    print("""
    Okay! Everything is done.
    You just need to update a few things...

    1. Update your main urls file to capture the app underneath it
        e.g.
        urlpatterns += patterns('',
            url(r'^', include('{}.{}.urls')),
            ...
        )
        - or -
        Update the `ROOT_URLCONF` option in the django settings file
        to reference your specific app.

    2. Add the app to your settings.py INSTALLED_APPS
    3. Add any dependencies to your settings.py INSTALLED_APPS
        Bootstrap3, and FactoryBoy are both currently necessary dependencies
        That you'll need to install (e.g. `sudo pip install X`)
    4. Sync/migrate your models and install the fixture data!
        This is located in {settings}.
        The following command will get you going:
            `python manage.py syncdb --noinput &&
             python manage.py generate_fixtures`

    See the README for more details.

    """.format(project_name, app_name, settings=settings_file))


def new_app_django(fixture_data):
    """A quick util to access the generator from command line"""
    print('Generating app "{}" in project "{}"'.format(
        fixture_data['config']['app_name'],
        fixture_data['config']['project_root']))
    # TODO: add types for classes (with --type option, or config property),
    # instead of defaulting to django
    gen = generators['django'](fixture_data)
    gen.generate_all()


# Run when file is run
try:
    if not sys.argv[2]:
        print('No JSON arguments supplied.')
    if sys.argv[1] == '--json' and sys.argv[2].endswith('json'):
        json_file = sys.argv[2]
        with open(json_file, 'r') as json_data:
            fixture_data = dict(json.loads(json_data.read()))
            if fixture_data['config']['project_root']:
                from_scratch_django(fixture_data)
            else:
                new_app_django(fixture_data)
    else:
        print('`{}` is not a valid .json file'.format(sys.argv[2]))
except IndexError:
    print(('No arguments were specified.'
           ' Please provided a JSON file with'
           ' the `--json filename` parameter.'))
