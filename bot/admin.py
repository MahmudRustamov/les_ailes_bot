import os
from asgiref.sync import async_to_sync
from aiogram.types import BufferedInputFile
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from bot.apps import BotConfig
from bot.models.base import City
from bot.models.product import Product, Category
from bot.models.user import TelegramUser
from core import config


class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # ... (list_display, list_filter, search_fields, readonly_fields saqlanadi) ...
    list_display = ['id', 'caption_short', 'created_at']
    list_filter = ['created_at']
    search_fields = ['caption', 'file_id']
    readonly_fields = ['file_id', 'file_unique_id', 'created_at']

    def caption_short(self, obj):
        # ... (caption_short funksiyasi saqlanadi) ...
        if obj.caption:
            return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
        return '-'

    caption_short.short_description = "Caption"

    def save_model(self, request, obj, form, change):
        """Upload image to Telegram before saving"""
        if obj.temp_file and not obj.file_id:
            try:
                # 1. Fayl kursorini boshiga qaytarish (upload qilishdan oldin muhim)
                obj.temp_file.seek(0)

                # 2. ASYNC funksiyani SINXRON kontekstda async_to_sync yordamida chaqirish
                # Qo'lda loop yaratish kodi butunlay olib tashlanadi.
                file_id, file_unique_id = async_to_sync(self._upload_to_telegram_async)(
                    obj.temp_file, obj.caption
                )

                # Check if this image already exists
                existing = Product.objects.filter(file_unique_id=file_unique_id).first()
                if existing:
                    # Clean up temp file
                    obj.temp_file.delete(save=False)
                    self.message_user(
                        request,
                        f"This image already exists in the database (ID: {existing.id}). Telegram file_unique_id: {file_unique_id}. You can reuse the existing file_id: {existing.file_id}",
                        level='WARNING'
                    )
                    return  # Don't save the duplicate

                obj.file_id = file_id
                obj.file_unique_id = file_unique_id

                # Save the object
                super().save_model(request, obj, form, change)

                # Clean up temp file
                if obj.temp_file:
                    obj.temp_file.delete(save=False)

                self.message_user(
                    request,
                    f"✅ Image uploaded to Telegram successfully! File ID: {file_id}",
                    level='SUCCESS'
                )

            except Exception as e:
                # Clean up temp file
                if obj.temp_file:
                    obj.temp_file.delete(save=False)

                self.message_user(
                    request,
                    f"❌ Error uploading to Telegram: {str(e)}",
                    level='ERROR'
                )
                raise
        else:
            super().save_model(request, obj, form, change)

    # 3. YANFI ASYNC METOD (qo'lda loop boshqaruvisiz)
    async def _upload_to_telegram_async(self, file_field, caption=None):
        """
        ASYNC funksiya: Faylni Telegramga yuklaydi.
        """
        storage_chat_id = getattr(config, 'TELEGRAM_STORAGE_CHAT_ID', None)

        if not storage_chat_id:
            raise ValueError(
                "TELEGRAM_STORAGE_CHAT_ID not set in settings. "
                "Please add your Telegram user ID or channel ID to settings.py"
            )

        # Read file content (bu yerda fayl o'qiladi, chunki save_model da seek(0) qilingan)
        file_content = file_field.read()
        file_name = os.path.basename(file_field.name)

        input_file = BufferedInputFile(
            file=file_content,
            filename=file_name
        )

        # To'g'ridan-to'g'ri asinxron yuborish
        result = await self._send_to_telegram(
            BotConfig.bot,
            storage_chat_id,
            input_file,
            caption
        )

        return result['file_id'], result['file_unique_id']

    @staticmethod
    async def _send_to_telegram(bot, chat_id, input_file, caption):
        """Send photo to Telegram and return file info"""
        message = await bot.send_photo(
            chat_id=chat_id,
            photo=input_file,
            caption=caption
        )

        return {
            'file_id': message.photo[-1].file_id,
            'file_unique_id': message.photo[-1].file_unique_id
        }


@admin.register(Category)
class CategoryAdmin(MyTranslationAdmin):
    list_display = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']


@admin.register(City)
class CityAdmin(MyTranslationAdmin):
    list_display = ['id', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(TelegramUser)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'username', 'first_name', 'last_name', 'phone_number', 'language_code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['username']