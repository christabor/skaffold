import factory
from . import models

{%% for model_name, props in all_models.iteritems() %%}
{%% set model_name = model_name|capitalize %%}
class {{{ model_name }}}Factory(factory.django.DjangoModelFactory):
    FACTORY_FOR = '{{{ model_name }}}'
    {%% for prop, value in props.iteritems() %%}{{{ prop }}} = {{{ value|get_modelfactory_field_type }}}{%% endfor %%}
{%% endfor %%}

def generate_test_data():
    MAX_RECORDS = 10
    for _ in xrange(MAX_RECORDS):
        {%% for model_name in all_models %%}{%% set model_name = model_name|capitalize %%}
        {{{ model_name }}}Factory()
        {%% endfor %%}
