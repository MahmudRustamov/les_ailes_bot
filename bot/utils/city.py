from asgiref.sync import sync_to_async

from bot.models.base import City


@sync_to_async
def get_all_cities(status=True):
    """Get all products from database"""
    return list(City.objects.all())