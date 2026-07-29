from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from locales import ru, en, kg

LOCALES = {"ru": ru.texts, "en": en.texts, "kg": kg.texts}
DEFAULT_LANG = "ru"


class I18nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        fsm_context = data.get("state")
        lang = DEFAULT_LANG

        if fsm_context:
            state_data = await fsm_context.get_data()
            lang = state_data.get("lang", DEFAULT_LANG)

        data["t"] = LOCALES.get(lang, LOCALES[DEFAULT_LANG])
        data["lang"] = lang
        return await handler(event, data)
