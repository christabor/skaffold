from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import models
import forms

def index(request):
    return render(request, 'pages/index.html')

{%% for model_name in all_models %%}{%% set model_name = model_name|capitalize %%}
def {{{ model_name|lower }}}(request):
    if request.method == 'POST':
        form = forms.{{{ model_name }}}Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added new {{{ model_name }}}')
    else:
        form = forms.{{{ model_name }}}Form()
    context = {
        'templates': models.{{{ model_name }}}.objects.all(),
        'form': form
    }
    return render(request, 'layouts/collection.html', context)


def {{{ model_name|lower }}}_detail(request, pk):
    if request.method == 'POST':
        form = forms.{{{ model_name }}}Form(
            request.POST, request.FILES, instance=context['template'])
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully edited {{{ model_name }}} details')
            return HttpResponseRedirect(request.path)
    else:
        form = forms.{{{ model_name }}}Form(instance=context['template'])
    return render(request, 'layouts/model.html', {'form': form})


def {{{ model_name|lower }}}_add(request, pk):
    # TODO
    pass


def {{{ model_name|lower }}}_delete(request, pk):
    try:
        {{{ model_name }}}.get(pk=pk).delete()
    except {{{ model_name }}}.DoesNotExist:
        pass
    pass
{%% endfor %%}
