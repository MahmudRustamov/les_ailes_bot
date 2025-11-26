import logging

from aiogram import Bot, Dispatcher
from django.apps import AppConfig

from core import config

logger = logging.getLogger(__name__)


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    bot: Bot = None
    dp: Dispatcher = None

    def ready(self):
        """Initialize bot and dispatcher when Django starts"""
        if not BotConfig.bot:
            logger.info("Initializing bot...")

            BotConfig.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            BotConfig.dp = Dispatcher()

            # Register middleware
            from bot.middlewares.i18n import TranslationMiddleware
            BotConfig.dp.message.middleware(TranslationMiddleware())
            BotConfig.dp.callback_query.middleware(TranslationMiddleware())

            # Register handlers
            from bot.handlers import start
            BotConfig.dp.include_router(start.router)

            logger.info("Bot initialized successfully with i18n support")