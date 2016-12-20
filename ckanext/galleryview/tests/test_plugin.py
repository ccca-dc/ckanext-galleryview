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
from ckan.tests.legacy import WsgiAppCase
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
        config['ckan.views.default_views'] = ('')
        app = ckan.config.middleware.make_app(config['global_conf'], **config)
        cls.app = paste.fixture.TestApp(app)

        ckan.plugins.load('galleryview')

        cls.dataset = factories.Dataset()
        cls.resource = factories.Resource(package_id=cls.dataset['id'])
        cls.sysadmin = factories.Sysadmin()

        cls.context = {'model': model,
                       'session': model.Session,
                       'user': cls.sysadmin['name']}

        cls.resource_view_dict = {'resource_id': cls.resource['id'],
                                  'view_type': 'gallery_view',
                                  'title': 'Gallery Test View',
                                  'description': 'A nice test view',
                                  'fields': ['http://some.image.png', 'another.image', '', 'http://different.image.png'],
                                  'image_names': ['some', 'another', 'test image', '']}

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

    def test_view_shown_in_resource_view_list(self):
        resource_view_list = tests.call_action_api(self.app,
                                                   'resource_view_list',
                                                   id=self.resource['id'],
                                                   apikey=self.sysadmin['apikey'])

        assert_equal(len(resource_view_list), 1)
        assert_equal(resource_view_list[0]['view_type'], 'gallery_view')

    def test_all_fields_saved(self):
        resource_view = tests.call_action_api(self.app,
                                              'resource_view_show',
                                              id=self.resource_view['id'],
                                              apikey=self.sysadmin['apikey'])

        assert_equal(self.resource_view_dict['fields'],
                     resource_view['fields'])
        assert_equal(resource_view['title'], 'Gallery Test View')
        assert_equal(resource_view['description'], 'A nice test view')
        assert_equal(resource_view['view_type'], 'gallery_view')

    def test_view_with_no_image_url(self):
        resource_view_dict = {'resource_id': self.resource['id'],
                                  'view_type': 'gallery_view',
                                  'title': 'Test View',
                                  'description': 'A nice test view',
                                  'fields': '',
                                  'image_names': ''}

        resource_view = tests.call_action_api(self.app,
                                              'resource_view_create',
                                              apikey=self.sysadmin['apikey'],
                                              **resource_view_dict)

        resource_view_show = tests.call_action_api(self.app,
                                                   'resource_view_show',
                                                   id=resource_view['id'],
                                                   apikey=self.sysadmin['apikey'])

        with assert_raises(KeyError):
            resource_view_show['fields']

    def test_view_update(self):
        resource_view_dict = {'resource_id': self.resource['id'],
                              'view_type': 'gallery_view',
                              'title': 'Gallery Test View',
                              'description': 'A nice test view',
                              'fields': ['http://some.image.png', 'another.image', 'http://test.image.png'],
                              'image_names': ['some', 'another', 'test image']}

        tests.call_action_api(self.app,
                              'resource_view_update',
                              id=self.resource_view['id'],
                              apikey=self.sysadmin['apikey'],
                                              **resource_view_dict)

        url = url_for(controller='package', action='resource_read',
                      id=self.dataset['name'], resource_id=self.resource['id'])
        response = self.app.get(url)

        assert_true(self.resource_view_dict['fields'][3] not in response)
        assert_true(resource_view_dict['fields'][2] in response)

    def test_gallery_view_html(self):
        url = url_for(controller='package', action='resource_read',
                      id=self.dataset['name'], resource_id=self.resource['id'])
        response = self.app.get(url)

        assert_true(self.resource_view_dict['fields'][0] in response)
        assert_true(self.resource_view_dict['image_names'][0] in response)
        assert_true(self.resource_view_dict['fields'][1] in response)
        assert_true(self.resource_view_dict['fields'][3] in response)
        assert_true(self.resource_view_dict['fields'][2] in response)

        url = url_for(controller='package', action='edit_view',
                      id=self.dataset['name'], resource_id=self.resource['id'],
                      view_id=self.resource_view['id'])

        # response = app.get(url)
        # log.debug(response)

        # testing of the edit view html but it has a context problem
