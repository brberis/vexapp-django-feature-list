from django.contrib import admin
from .models import Features, FeatureList
from parler.admin import TranslatableAdmin, TranslatableTabularInline
from aldryn_translation_tools.admin import AllTranslationsMixin


class FeaturesAdmin(AllTranslationsMixin, TranslatableAdmin):

    list_display = ('title', 'icon_class', 'description', 'active')

class FeaturesInline(TranslatableTabularInline):
    model = Features


class FeatureListAdmin(AllTranslationsMixin, TranslatableAdmin):

    list_display = ('title', 'description', 'featured_image', 'active')
    inlines = [
        FeaturesInline,
    ]





# Register your models here.
admin.site.register(FeatureList, FeatureListAdmin)
admin.site.register(Features, FeaturesAdmin)
