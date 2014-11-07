from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

{%% set app_name = app_name|lower %%}
urlpatterns = patterns('',
    ('^$', '{{{ app_name }}}.views.index'),
    {%% for model_name in all_models %%}{%% set model_name = model_name|lower %%}
    ('^{{{ model_name }}}/$', '{{{ app_name }}}.views.{{{ model_name }}}'),
    ('^{{{ model_name }}}/delete$', '{{{ app_name }}}.views.{{{ model_name }}}_delete'),
    ('^{{{ model_name }}}/add$', '{{{ app_name }}}.views.{{{ model_name }}}_add'),
    ('^{{{ model_name }}}/(?P<id>[0-9])/$', '{{{ app_name }}}.views.{{{ model_name }}}'),
    {%% endfor %%}
    url('^admin/', include(admin.site.urls)),
)
