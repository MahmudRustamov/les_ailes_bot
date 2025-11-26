from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from bot.models.base import City


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)