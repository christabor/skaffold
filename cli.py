import os
import sys
import json
import skaffolding


__types__ = {
    'django': skaffolding.DjangoGenerator,
    'flask': skaffolding.FlaskGenerator,
}


def from_scratch_django(fixture_data):
    """Does all work required to setup a completely new application."""
    project_name = fixture_data['config']['project_root']
    app_name = fixture_data['config']['app_name']

    # TODO: this is kind of weird

    print('Deleting existing django project (if applicable)...')
    os.system('rm -r ' + project_name)

    print('Adding new django project...')
    os.system('django-admin.py startproject ' + project_name)

    print('Generating new django app...')
    new_app_django(fixture_data)

    print('Generating DB tables...')
    os.system('cd ' + project_name + ' && python manage.py syncdb --noinput')

    print('Generating DB test data...')
    os.system('python manage.py generate_fixtures')

    print('Jumping back down...')
    os.system('cd ..')

    # TODO: Automatically fix the below issues for user.
    # TODO: test with making a bunch of apps, in config

    print("""
    Okay! Everything is done.
    You just need to update a few things...

    1. Update your main urls file to capture the app underneath it
        e.g.
        urlpatterns += patterns('',
            (r'^', include('{}.{}.urls')),
        )

    2. Add the app to your settings.py INSTALLED_APPS
    3. Add any dependencies to your settings.py INSTALLED_APPS

    See the README for more details.

    """.format(project_name, app_name))


def new_app_django(fixture_data):
    """A quick util to access the generator from command line"""
    print('Generating... app "{}" in project "{}"'.format(
        fixture_data['config']['app_name'],
        fixture_data['config']['project_root']))

    # TODO: add types for classes (with --type option, or config property),
    # instead of defaulting to django
    gen = __types__['django'](fixture_data)
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
