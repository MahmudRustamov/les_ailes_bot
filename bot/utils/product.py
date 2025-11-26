from asgiref.sync import sync_to_async

from bot.models.product import Product


@sync_to_async
def get_all_products(status=True):
    """Get all products from database"""
    return list(Product.objects.filter(status=status))