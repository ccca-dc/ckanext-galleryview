import os
import shutil

import ckan.lib.helpers as h
import ckan.lib.base as base
import requests
from pylons import config
import ckan.plugins.toolkit as toolkit

import cgi
import logging
import json
import pathlib2
import ckan.model as model
import ckan.logic as logic
import ckan.lib.uploader as uploader
import pprint
import ast
import ckan.lib.navl.dictization_functions as dict_fns
from ckan.common import OrderedDict, c, g, request, _

get_action = logic.get_action
parse_params = logic.parse_params
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
abort = base.abort

check_access = logic.check_access

# c = base.c
request = base.request
log = logging.getLogger(__name__)


class UploadController(base.BaseController):

    def image_upload(self):
        filedata = request.POST.get('file-0')
        data_dict = request.POST.get('dict')
        resource_id = request.POST.get('resource_id')

        context = {'model': model, 'session': model.Session,
                   'user': c.user}
        try:
            check_access('resource_view_update', context, {'id': resource_id})
        except NotAuthorized:
            abort(403, _('Unauthorized to upload image'))

        data_dict = {}
        data_dict['file'] = filedata
        data_dict['image_url'] = ''
        data_dict['clear_upload'] = ''
        upload = uploader.get_uploader('gallery/' + resource_id + "/")
        try:
            upload.update_data_dict(data_dict, 'image_url',
                                    'file', 'clear_upload')
            upload.upload()

            return data_dict['image_url']
        except ValidationError:
            pass

    def image_delete(self):
        resource_id = request.POST.get('resource_id')
        image_url = request.POST.get('image_url')

        context = {'model': model, 'session': model.Session,
                   'user': c.user}
        try:
            check_access('resource_view_update', context, {'id': resource_id})
        except NotAuthorized:
            abort(403, _('Unauthorized to delete image'))

        storage_path = config.get('ckan.storage_path')
        file_path = storage_path + '/storage/uploads/gallery/' + resource_id
        images_stored = os.listdir(file_path)

        if image_url in images_stored:
            os.remove(file_path + '/' + image_url)
