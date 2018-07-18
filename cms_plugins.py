# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms import __version__ as cms_version
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models



class TemplatePrefixMixin(object):

    def get_render_template(self, context, instance, placeholder):

        return self.render_template


class FeaturesPlugin(TemplatePrefixMixin, CMSPluginBase):
    module = 'RE Plugins'

@plugin_pool.register_plugin
class FeatureListPlugin(FeaturesPlugin):
    render_template = 'feature_list/feature_list.html'
    name = _('Feature List')
    model = models.FeatureListPlugin



    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['feature_list'] = instance.get_feature_list(request)
        context['features'] = instance.get_features(request)
        return context
