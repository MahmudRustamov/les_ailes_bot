import logging

from aiogram import Bot, Dispatcher
from django.apps import AppConfig

from bot.handlers import auth
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
            from bot.handlers import start, menu, backs, order
            BotConfig.dp.include_router(start.router)
            BotConfig.dp.include_router(menu.router)
            BotConfig.dp.include_router(backs.router)
            BotConfig.dp.include_router(order.router)
            BotConfig.dp.include_router(auth.router)

            logger.info("Bot initialized successfully with i18n support")