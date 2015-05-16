from django.test import TestCase
{%% for model_name in all_models %%}
{%% set model_name = model_name|lower %%}
class {{{ model_name|capitalize }}}CRUDTestCase(TestCase):

    def setUp(self):
        pass

    def test_{{{ model_name }}}_edit(self):
        # TODO: must implement
        self.assertTrue(False)

    def test_{{{ model_name }}}_edit_bad_input(self):
        # TODO: must implement
        self.assertTrue(False)

    def test_{{{ model_name }}}_delete(self):
        # TODO: must implement
        self.assertTrue(False)

    def test_{{{ model_name }}}_view(self):
        # TODO: must implement
        self.assertTrue(False)

    def tearDown(self):
        pass
{%% endfor %%}
