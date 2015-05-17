from django import forms
import models

{%% for model_name, fields in all_models.iteritems() %%}
{%% set model_name = model_name|capitalize %%}

class {{{ model_name }}}Form(forms.ModelForm):
    class Meta:
        fields = [{%% for prop, value in fields.iteritems() %%}'{{{ prop }}}', {%% endfor %%}]
        model = models.{{{ model_name }}}

{%% endfor %%}
