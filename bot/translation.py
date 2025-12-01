from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions
from bot.models.base import City
from bot.models.product import Category


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CityTranslationOptions(TranslationOptions):
    fields = ('title',)