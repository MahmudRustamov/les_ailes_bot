from asgiref.sync import sync_to_async

from bot.models.product import Product, Category


@sync_to_async
def get_all_products(status=True):
    """Get all products from database"""
    return list(Product.objects.filter(status=status))


@sync_to_async
def get_all_categories(status=True):
    """Get all products from database"""
    return list(Category.objects.all())