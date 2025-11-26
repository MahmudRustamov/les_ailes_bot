import logging

from asgiref.sync import sync_to_async


from datetime import datetime


def add_user(data: dict):
    return User.objects.create(
        full_name=data.get("full_name"),
        phone_number=data.get("phone_number"),
        chat_id=data.get("chat_id"),
        city=data.get("city"),
        language=data.get("language"),
        created_at=data.get("created_at") or datetime.utcnow(),
        updated_at=data.get("created_at") or datetime.utcnow()
    )


async def get_user(chat_id: int):
    try:
        user = await User.objects.filter(chat_id=chat_id).afirst()
        return user
    except Exception as e:
        error_text = f"Error appeared when getting user: {e}"
        logging.error(error_text)
        return None


async def get_language(chat_id: int, default_lang: str = "en"):
    try:
        if chat_id is None:
            return default_lang

        user = await sync_to_async(User.objects.filter(chat_id=chat_id).first)()
        if user and getattr(user, 'language', None):
            return user.language

        return default_lang

    except Exception as e:
        logging.error(f"Error appeared when getting user: {e}")
        return default_lang


async def change_user_name(chat_id: int, new_name: str):
    try:
        user = await sync_to_async(User.objects.filter(chat_id=chat_id).first)()
        if user and getattr(user, 'language', None):
            return user.language

    except Exception as e:
        logging.error(f"Error appeared when getting user: {e}")
        return