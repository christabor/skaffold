from django.db import models
from django.utils.translation import ugettext_lazy as _


{%% for model_name, props in all_models.iteritems() %%}
{%% set model_name = model_name|capitalize %%}
class {{{ model_name }}}(models.Model):
    {%% for prop, value in props.iteritems() %%}
    {{{ prop }}} = {{{ value|model_field }}}
    {%% endfor %%}
    def __unicode__(self):
        return unicode()
{%% endfor %%}
