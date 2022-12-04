import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan import model


def get_groups():
    groups = toolkit.get_action('group_list')(data_dict={'all_fields': True})
    return groups


def get_latest_packages():
    resources = toolkit.get_action('current_package_list_with_resources')(data_dict={
        'limit': 3,
        'offset': 0,
    })
    return resources


def get_visualizations():
    # values = model.Session.query(model.ResourceView).filter_by(view_type='visualize').all()
    values = model.Session.query(model.ResourceView) \
        .filter(model.ResourceView.view_type.in_(['image_view'])) \
        .all()
    response = list(map(lambda x: x.as_dict(), values))
    response.reverse()
    for i in response:
        resource = toolkit.get_action('resource_show')(
            data_dict={'id': i['resource_id']})
        i['resource'] = resource
    return response[0:5]

def get_category_total():
    return model.Session.query(model.Group) \
        .count()

def get_resource_total():
    return model.Session.query(model.Resource) \
        .count()


class InegtPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'inegt')
        toolkit.add_resource('assets', 'ine_style')

    # ITemplateHelpers
    def get_helpers(self):
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'ine_groups': get_groups,
            'ine_latest_packages': get_latest_packages,
            'ine_visualizations': get_visualizations,
            'ine_category_total': get_category_total,
            'ine_resource_total': get_resource_total,
        }