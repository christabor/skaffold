from django import forms
import models

{%% for model_name in all_models %%}
{%% set model_name = model_name|capitalize %%}
class {{{ model_name }}}Form(forms.ModelForm):

    class Meta:
        model = models.{{{ model_name }}}
{%% endfor %%}
