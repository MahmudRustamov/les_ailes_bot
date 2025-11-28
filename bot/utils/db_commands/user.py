from asgiref.sync import sync_to_async
from bot.models.user import TelegramUser


@sync_to_async
def update_user_city(user_id, city: str):
    user = TelegramUser.objects.get(user_id=user_id)
    user.city = city
    user.save(update_fields=['city'])
    return user