"""Tests for plugin.py."""
import ckanext.galleryview.plugin as plugin

from nose.tools import assert_true
from nose.tools import assert_raises
from nose.tools import assert_equal
from nose.tools import assert_in
from ckan.tests import helpers, factories
from ckan.tests.legacy.html_check import HtmlCheckMethods

import paste.fixture
import pylons.test
import webtest

import logging

import ckan.model as model
import ckan.tests.legacy as tests
import ckan.plugins
import ckan.logic as logic
from ckan.common import config

from routes import url_for

log = logging.getLogger(__name__)


class TestGalleryView(object):

    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('galleryview')

        dataset = factories.Dataset()
        cls.resource = factories.Resource(package_id=dataset['id'])
        sysadmin = factories.Sysadmin()

        cls.context = {'model': model,
                       'session': model.Session,
                       'user': sysadmin['name']}

        cls.resource_view_dict = {'resource_id': cls.resource['id'],
                                  'view_type': 'galleryview',
                                  'title': 'Gallery Test View',
                                  'description': 'A nice test view',
                                  'fields': ['http://some.image.png', 'http://another.png'],
                                  'image_names': ['some', 'another']}

        cls.resource_view = ckan.plugins.toolkit.get_action('resource_view_create')(
            cls.context, cls.resource_view_dict)


    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
        have been run.
        '''
        # We have to unload the plugin we loaded, so it doesn't affect any
        # tests that run after ours.
        model.repo.rebuild_db()
        ckan.plugins.unload('galleryview')

    @helpers.change_config('ckan.views.default_views', '')
    def test_view_shown_in_resource_view_list(self):
        resource_view_list = ckan.plugins.toolkit.get_action('resource_view_list')(
            self.context, {'id': self.resource['id']})

        assert_equal(len(resource_view_list), 1)
        assert_equal(resource_view_list[0]['view_type'], 'galleryview')

    def test_all_fields_saved(self):
        resource_view_show = ckan.plugins.toolkit.get_action('resource_view_show')(
            self.context, {'id': self.resource_view['id']})

        assert_equal(self.resource_view_dict['fields'],
                     resource_view_show['fields'])
        assert_equal(resource_view_show['title'], 'Gallery Test View')
        assert_equal(resource_view_show['description'], 'A nice test view')
        assert_equal(resource_view_show['view_type'], 'galleryview')

    def test_view_with_no_image_url(self):
        resource_view_dict = {'resource_id': self.resource['id'],
                                  'view_type': 'galleryview',
                                  'title': 'Test View',
                                  'description': 'A nice test view',
                                  'fields': '',
                                  'image_names': ''}

        resource_view = ckan.plugins.toolkit.get_action('resource_view_create')(
            self.context, resource_view_dict)

        resource_view_show = ckan.plugins.toolkit.get_action('resource_view_show')(
            self.context, {'id': resource_view['id']})

        with assert_raises(KeyError):
            resource_view_show['fields']


class TestGalleryViewHtml(helpers.FunctionalTestBase):

    @classmethod
    def setup_class(cls):

        super(TestGalleryViewHtml, cls).setup_class()
        config['ckan.views.default_views'] = ('')

        ckan.plugins.load('galleryview')

    @classmethod
    def teardown_class(cls):
        ckan.plugins.unload('galleryview')

        super(TestGalleryViewHtml, cls).teardown_class()

        # model.repo.rebuild_db()
        helpers.reset_db()

    def test_gallery_view(self):
        app = helpers._get_test_app()

        dataset = factories.Dataset()
        resource = factories.Resource(package_id=dataset['id'])
        sysadmin = factories.Sysadmin()

        context = {'model': model,
                   'session': model.Session,
                   'user': sysadmin['name']}

        resource_view_dict = {'resource_id': resource['id'],
                                  'view_type': 'galleryview',
                                  'title': 'Gallery Test View',
                                  'description': 'A nice test view',
                                  'fields': ['http://some.image.png',
                                             'another.image'],
                                  'image_names': ['some', 'another']}

        resource_view = helpers.call_action('resource_view_create', context,
                                            **resource_view_dict)

        url = url_for(controller='package', action='resource_read',
                      id=dataset['name'], resource_id=resource['id'])
        response = app.get(url)

        assert_true(resource_view_dict['fields'][0] in response)
        assert_true(resource_view_dict['image_names'][0] in response)
        assert_true(resource_view_dict['fields'][1] in response)

        url = url_for(controller='package', action='edit_view',
                      id=dataset['name'], resource_id=resource['id'],
                      view_id=resource_view['id'])

        # response = app.get(url)
        # log.debug(response)

        # testing of the edit view html but it has a context problem
