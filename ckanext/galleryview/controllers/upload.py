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
        data_dict['image_url'] = ''
        data_dict['clear_upload'] = ''
        upload = uploader.get_uploader('gallery/' + resource_id + "/")
        upload.update_data_dict(data_dict, 'image_url',
                                'file', 'clear_upload')
        upload.upload()
        return data_dict['image_url']

    def image_delete(self):
        resource_id = request.POST.get('resource_id')
        image_url = request.POST.get('image_url')
        storage_path = config.get('ckan.storage_path')
        file_path = storage_path + '/storage/uploads/gallery/' + resource_id + '/' + image_url
        os.remove(file_path)
