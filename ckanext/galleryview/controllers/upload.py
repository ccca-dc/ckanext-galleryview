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

get_action = logic.get_action
parse_params = logic.parse_params
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict

c = base.c
request = base.request
log = logging.getLogger(__name__)


class UploadController(base.BaseController):

    def image_upload(self):
        filedata = request.POST.get('file-0')
        data_dict = request.POST.get('dict')
        resource_id = request.POST.get('resource_id')
        data_dict = ast.literal_eval(data_dict)
        data_dict['file'] = filedata
        log.debug('gallery/' + resource_id + "/")
        upload = uploader.get_uploader('gallery/' + resource_id + "/")
        upload.update_data_dict(data_dict, 'image_url',
                                'file', 'clear_upload')
        upload.upload()
        log.debug(pprint.pprint(data_dict))

    def image_delete(self):
        data_dict = request.POST.get('dict')
        data_dict = ast.literal_eval(data_dict)
        data_dict['clear_upload'] = "true"
        resource_id = data_dict.get('resource_id')
        image_url = data_dict.get('image_url')
        upload = uploader.get_uploader('gallery/' + resource_id)
        upload.update_data_dict(data_dict, 'image_url',
                                'file', 'clear_upload')
        upload.upload()
        storage_path = config.get('ckan.storage_path')
        file_path = storage_path + '/gallery/' + resource_id + '/' + image_url
        log.debug(pprint.pprint(file_path))
        os.remove(file_path)
