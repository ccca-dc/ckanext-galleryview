import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import pprint

log = logging.getLogger(__name__)

ignore_empty = plugins.toolkit.get_validator('ignore_empty')

DEFAULT_IMAGE_FORMATS = ['png', 'jpeg', 'jpg', 'gif']


class GalleryviewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'galleryview')

    def info(self):
        return {'name': 'gallery_view',
                'title': plugins.toolkit._('Gallery'),
                'icon': 'picture',
                'schema': {
                    'fields': [ignore_empty],
                    'image_names': [ignore_empty]
                    },
                'iframed': False,
                'always_available': True,
                'default_title': plugins.toolkit._('Gallery'),
                'preview_enabled': True
                }

    def can_view(self, data_dict):
        return (data_dict['resource'].get('format', '').lower()
                in DEFAULT_IMAGE_FORMATS)

    def view_template(self, context, data_dict):
        return 'gallery_view.html'

    def form_template(self, context, data_dict):
        log.debug(data_dict)
        return 'gallery_form.html'

    def setup_template_variables(self, context, data_dict):
        """Setup variables available to templates"""

        fields = data_dict['resource_view'].get('fields', '')
        image_names = data_dict['resource_view'].get('image_names', '')

        fieldoutput = []
        imgs = []

        if type(fields) is list:
            fieldoutput = fields
            imgs = image_names
        else:
            fieldoutput.append(fields)
            imgs.append(image_names)

        tpl_variables = {
            'urls': fieldoutput,
            'imgs': imgs
        }

        return tpl_variables
