from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

{%% set app_name = app_name|lower %%}
urlpatterns = patterns('{{{ project_root }}}.{{{ app_name }}}.views',
    url(r'^$', 'render_static', {'page': 'index'}),
    {%% for model_name in all_models %%}{%% set model_name = model_name|lower %%}
    url(r'^{{{ model_name }}}/$', '{{{ model_name }}}'),
    url(r'^{{{ model_name }}}/add/$', '{{{ model_name }}}_add'),
    url(r'^{{{ model_name }}}/(?P<pk>[0-9]+)/$', '{{{ model_name }}}_detail'),
    url(r'^{{{ model_name }}}/(?P<pk>[0-9]+)/delete/$', '{{{ model_name }}}_delete'),
    {%% endfor %%}
    {%% for _, staticpage in staticpages.iteritems() %%}{%% set staticpage = staticpage|lower %%}
    url(r'^{{{ staticpage }}}/$', 'render_static', {'page': '{{{ staticpage }}}'}),
    {%% endfor %%}
    {%% if use_admin %%}url(r'^admin/', include(admin.site.urls)),{%% endif %%}
)
