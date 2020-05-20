from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from django.utils import translation


# Create your models here.


class FeaturesManager(TranslatableManager):
    def active(self, **kwargs):
        return self.filter(active=True, **kwargs)

class FeatureList(TranslatableModel):

    featured_image = FilerImageField(on_delete=models.CASCADE, null=True, blank=True,related_name="main_feature_image")
    active = models.BooleanField(_('Activa'), default=True)
    translations = TranslatedFields(
    title = models.CharField(max_length=150, verbose_name=_('Titles'), null=True, blank=True),
    description = models.TextField(verbose_name=_('Descripcion'), null=True, blank=True),
    )
 
    def __str__(self):
        return self.title

    class Meta:
            verbose_name = _('Feature List')
            verbose_name_plural = _('Feature Lists')

class Features(TranslatableModel):
    feature_list = models.ForeignKey(FeatureList, null=True, blank=True, related_name='features', on_delete=models.CASCADE)
    icon_class = models.CharField(_('Icon class'), max_length=100, help_text=_('Enter Awesome icon class name.')
    )
    active = models.BooleanField(_('Activa'), default=True)
    translations = TranslatedFields(
    title = models.CharField(max_length=150, verbose_name=_('Titles'), null=True, blank=True),
    description = models.TextField(verbose_name=_('Descripcion'), null=True, blank=True),
    )
 
    def __str__(self):
        return self.title

    class Meta:
            verbose_name = _('Feature')
            verbose_name_plural = _('Features')

class PluginEditModeMixin(object):
    def get_edit_mode(self, request):
        """
        Returns True only if an operator is logged-into the CMS and is in
        edit mode.
        """
        return (
            hasattr(request, 'toolbar') and request.toolbar and
            request.toolbar.edit_mode)

class FeaturesCMSPlugin(CMSPlugin):
    """AppHookConfig aware abstract CMSPlugin class for Aldryn Newsblog"""
    # avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True, on_delete=models.CASCADE)


    class Meta:
        abstract = True

class FeatureListPlugin(PluginEditModeMixin,
                                   FeaturesCMSPlugin):
    
    # translation.activate('en')
    feature_title = models.ForeignKey(FeatureList, null=True, blank=True,
        help_text=_('Select Feature List to show'), on_delete=models.CASCADE
    )


    def get_features(self, request):
        queryset = Features.objects.all().filter(active=True).filter(feature_list = self.feature_title)
        return queryset

    def get_feature_list(self, request):
        queryset = FeatureList.objects
        queryset = FeatureList.objects.all().filter(active=True).translated(title = self.feature_title)
        return queryset


