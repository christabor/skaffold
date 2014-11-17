from factory import fuzzy
from factory import django
from . import models

{%% for model_name, props in all_models.iteritems() %%}{%% set model_name = model_name|capitalize %%}
class {{{ model_name }}}Factory(django.DjangoModelFactory):
    class Meta:
        model = models.{{{ model_name }}}
    {%% for prop, value in props.iteritems() %%}
    {{{ prop }}} = {{{ value|factory_field }}}
    {%% endfor %%}
{%% endfor %%}
