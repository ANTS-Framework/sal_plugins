from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings

class ANTS_Status(IPlugin):
    # def plugin_type(self):
    #     return 'condition'

    def widget_width(self):
        return 4

    def get_description(self):
        return 'ANTS Status'

    def widget_content(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('plugins/traffic_lights_front.html')

        if page == 'bu_dashboard':
            t = loader.get_template('plugins/traffic_lights_id.html')

        if page == 'group_dashboard':
            t = loader.get_template('plugins/traffic_lights_id.html')

        try:
            ants_status_ok = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='ok').count()
        except:
            ants_status_ok = 0

        try:
            ants_status_changed = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='changed').count()
        except:
            ants_status_changed = 0

        try:
            ants_status_failed = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='failed').count()
        except:
            ants_status_failed = 0

        c = Context({
            'title': self.get_description(),
            'ok_label': 'ok',
            'ok_count': ants_status_ok,
            'warning_label': 'changed',
            'warning_count': ants_status_changed,
            'alert_label': 'failed',
            'alert_count': ants_status_failed,
            'plugin': 'ANTS_Status',
            'theid': theid,
            'page': page
        })
        return t.render(c)

    def filter_machines(self, machines, data):
        if data == 'ok':
            machines = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='ok')
            title = 'Machines with unchanged state'
        elif data == 'warning':
            machines = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='changed')
            title = 'Machines with changed state'
        elif data == 'alert':
            machines = machines.filter(
                conditions__condition_name='ants_status',
                conditions__condition_data__startswith='failed')
            title = 'Machines with ansible errors'
        else:
            machines = None
            title = None

        return machines, title
