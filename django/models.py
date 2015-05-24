from django.db import models
from django.utils.translation import ugettext_lazy as _

{%% for model_name, props in all_models.iteritems() %%}
{%% set model_name = model_name|capitalize %%}

class {{{ model_name }}}(models.Model):
    {%% for prop, value in props.iteritems() %%}
    {%% if value == '__M2M__' %%}
    {{{ prop }}} = models.ManyToManyField('{{{ prop|capitalize }}}', blank=True)
    {%% elif value|is_list %%}
    {{{ prop|pluralize }}} = (
        {%% for option in value %%}
        ('{{{ option|first|capitalize }}}', '{{{ option }}}'),
        {%% endfor %%}
    )
    {{{ prop }}} = models.CharField(
        max_length=50, blank=False, choices={{{ prop|pluralize }}})
    {%% elif value == '__DATE__' %%}
    {{{ prop }}} = models.DateTimeField()
    {%% elif value == '__FILE__' %%}
    {{{ prop }}} = models.FileField(
        help_text='Upload your {{{ prop|pluralize }}} here.',
        upload_to='{{{ upload_dir }}}{{{ prop|pluralize }}}/', max_length=1000)
    {%% else %%}
    {{{ prop }}} = {{{ value|model_field }}}
    {%% endif %%}
    {%% endfor %%}

    def __unicode__(self):
        fields = [{%% for prop, value in props.iteritems() %%}'{{{ prop }}}', {%% endfor %%}]
        return unicode('<{%% for prop, value in props.iteritems() %%}{}.{%% endfor %%}>'.format(*fields))

{%% endfor %%}
