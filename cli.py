import os
import sys
import json
import collections
from skaffolders import DjangoSkaffolder

__author__ = """Chris Tabor (dxdstudio@gmail.com)"""


def _clean(root_dir):
    os.system('rm -r ' + root_dir)


def from_scratch_django(fixture_data, launch=True, verbose=False):
    """Does all work required to setup a completely new application."""
    django = DjangoSkaffolder(fixture_data)
    project_name = django.project_name
    app_name = django.app_name

    if verbose:
        print('Deleting existing project '
              '(if applicable) located at {}'.format(django.project_root))
    _clean(django.project_root)
    # Move into the newly created directory.
    os.chdir(django.abspath)
    # print('Adding new django project...')
    os.system('django-admin.py startproject ' + project_name)
    # Move into subdir (django project) to setup single app structure
    django.project_root = '{}{}/'.format(
        django.project_root, django.project_name)
    django.app_root = '{}{}/'.format(django.project_root, django.app_name)

    os.chdir(django.project_root)
    os.mkdir(django.app_root)
    # Setup template structure
    django.make_app_dirs()
    # Generate data for django *after* django creates the app.
    new_app_django(django, app_name, project_name)

    root_urlconf = django.project_root + 'urls.py'
    settings_file = django.project_root + 'settings.py'

    if verbose:
        print('Updating settings and urlconf files...')
    # Move extra settings up.
    os.rename(
        django.app_root + 'extra_settings.py',
        django.project_root + 'extra_settings.py')
    with open(settings_file, 'a') as django_settings:
        django_settings.write('from extra_settings import *\n')
        django_settings.close()

    with open(root_urlconf, 'a') as urlconf:
        urlconf.write(
            "\nfrom {app} import urls as {app}_urls\n"
            "urlpatterns += url(r'^', include({app}_urls)),\n".format(
                app=app_name))
        urlconf.close()

    os.chdir('../')
    if verbose:
        print('Creating database tables and fixture data...')
    os.system('python manage.py syncdb --noinput && '
              'python manage.py generate_fixtures')

    if launch:
        if verbose:
            print('Running server!')
        os.system('python manage.py runserver')

    print("""
    Okay! Everything is done.
    Now, check out the REDAME and example JSON configuration for more details.

    Happy Skaffolding!
    """.format(project_name, app_name, settings=settings_file))


def new_app_django(skaffold, app, project, verbose=False):
    """A quick util to access the generator from command line"""
    if verbose:
        print('Generating app "{}" in project "{}"'.format(app, project))
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
    if sys.argv[1] == '--json' and sys.argv[2].endswith('json'):
        can_launch = '--noserve' not in sys.argv
        verbose = '--verbose' in sys.argv
        json_file = sys.argv[2]
        with open('defaults.json', 'r') as default_json_data:
            json_config = dict(json.loads(default_json_data.read()))
            with open(json_file, 'r') as json_data:
                extra_config = dict(json.loads(json_data.read()))
                json_config = mergedicts(json_config, extra_config)
                if json_config['config']['project_root']:
                    from_scratch_django(
                        json_config, launch=can_launch, verbose=verbose)
                else:
                    app = json_config['config']['app_name']
                    project = json_config['config']['project_root']
                    new_app_django(
                        json_config, app, project, verbose=verbose)
    else:
        print('`{}` is not a valid .json file'.format(sys.argv[2]))
except IndexError:
    print(('No arguments were specified.'
           ' Please provided a JSON file with'
           ' the `--json filename` parameter.'))
