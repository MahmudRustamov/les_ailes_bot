from asgiref.sync import sync_to_async
from django.db.models import Q

from bot.models.base import City
from bot.models.product import Category


@sync_to_async
def get_all_cities(status=True):
    """Get all products from database"""
    return list(City.objects.all())


@sync_to_async
def get_city(city_name: str):
    """Get all matching cities"""
    return City.objects.filter(
        Q(name_uz__icontains=city_name) | Q(name_en__icontains=city_name)
    ).first()



