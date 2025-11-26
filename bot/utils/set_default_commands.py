from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Botni ishga tushurish")
        ],
        scope=BotCommandScopeDefault()
    )



