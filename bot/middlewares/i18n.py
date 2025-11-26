from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from django.utils.translation import activate

from bot.utils.translation import get_user_language


class TranslationMiddleware(BaseMiddleware):
    """Middleware to automatically set user's language for each update"""

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        # Get user_id from the event
        user_id = event.from_user.id

        # Activate user's language (await the async function)
        language = await get_user_language(user_id)
        activate(language)

        # Add translation info to data
        data['user_language'] = language

        # Call the handler
        return await handler(event, data)