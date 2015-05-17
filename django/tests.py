from django.test import TestCase

{%% for model_name in all_models %%}
{%% set model_name = model_name|lower %%}

class {{{ model_name|capitalize }}}CRUDTestCase(TestCase):

    def setUp(self):
        pass

    def test_{{{ model_name }}}_edit(self):
        raise NotImplementedError

    def test_{{{ model_name }}}_edit_bad_input(self):
        raise NotImplementedError

    def test_{{{ model_name }}}_delete(self):
        raise NotImplementedError

    def test_{{{ model_name }}}_view(self):
        raise NotImplementedError

    def tearDown(self):
        pass

{%% endfor %%}
