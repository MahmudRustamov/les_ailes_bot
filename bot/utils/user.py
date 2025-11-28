from asgiref.sync import sync_to_async

from bot.models.user import TelegramUser


@sync_to_async
def partial_update_user(data: dict, user_id: int):
    """Get all products from database"""
    return TelegramUser.objects.filter(
        user_id=user_id
    ).update(**data)