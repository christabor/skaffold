import os
import sys
import json
import collections
from skaffolders import FlaskSkaffolder
from skaffolders import DjangoSkaffolder


def _clean(root_dir):
    print('Deleting existing project (if applicable) located at {}'.format(
        root_dir))
    os.system('rm -r ' + root_dir)


def from_scratch_django(fixture_data, launch=True):
    """Does all work required to setup a completely new application."""
    project_name = fixture_data['config']['project_root']
    app_name = fixture_data['config']['app_name']
    root_dir = os.getcwd() + '/' + project_name + '/'
    root_urlconf = root_dir + '/' + project_name + '/urls.py'
    settings_file = root_dir + '/' + project_name + '/settings.py'

    _clean(root_dir)

    print('Adding new django project...')
    os.system('django-admin.py startproject ' + project_name)

    print('Skaffolding app structure...')
    django_skaffold = DjangoSkaffolder(fixture_data)
    new_app_django(django_skaffold, fixture_data)

    print('Updating settings and urlconf files...')
    with open(settings_file, 'a') as django_settings:
        django_settings.write(
            "\nINSTALLED_APPS += ('{project}.{app}', 'bootstrap3',)\n".format(
                project=project_name, app=app_name))
        django_settings.close()

    with open(root_urlconf, 'a') as urlconf:
        urlconf.write(
            "\nfrom {app} import urls as {app}_urls\n"
            "urlpatterns += url(r'^', include({app}_urls)),\n".format(
                app=app_name))
        urlconf.close()

    print('Creating database tables and fixture data...')
    os.system('cd {} && python manage.py syncdb --noinput && '
              'python manage.py generate_fixtures'.format(project_name))

    if launch:
        print('Running server!')
        os.system('cd {} && python manage.py runserver'.format(project_name))

    print("""
    Okay! Everything is done.
    Now, check out the REDAME and example JSON configuration for more details.

    Happy Skaffolding!
    """.format(project_name, app_name, settings=settings_file))


def new_app_django(skaffold, fixture_data):
    """A quick util to access the generator from command line"""
    print('Generating app "{}" in project "{}"'.format(
        fixture_data['config']['app_name'],
        fixture_data['config']['project_root']))
    skaffold.generate_all()


def mergedicts(d, u):
    """Credit: stackoverflow.com/questions/3232943
        /update-value-of-a-nested-dictionary-of-varying-depth"""
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = mergedicts(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


# Run when file is run
try:
    if not sys.argv[2]:
        print('No JSON arguments supplied.')
    print(sys.argv)
    if sys.argv[1] == '--json' and sys.argv[2].endswith('json'):
        can_launch = '--noserve' not in sys.argv
        json_file = sys.argv[2]
        with open('defaults.json', 'r') as default_json_data:
            json_config = dict(json.loads(default_json_data.read()))
            with open(json_file, 'r') as json_data:
                extra_config = dict(json.loads(json_data.read()))
                json_config = mergedicts(json_config, extra_config)
                if json_config['config']['project_root']:
                    from_scratch_django(json_config, launch=can_launch)
                else:
                    new_app_django(json_config)
    else:
        print('`{}` is not a valid .json file'.format(sys.argv[2]))
except IndexError:
    print(('No arguments were specified.'
           ' Please provided a JSON file with'
           ' the `--json filename` parameter.'))
