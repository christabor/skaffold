from django.contrib import admin
import models

{%% for model_name in all_models %%}
admin.site.register(models.{{{ model_name|capitalize }}})
{%% endfor %%}
