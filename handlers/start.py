from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main import language_kb, main_menu_kb
from locales import ru, en, kg

router = Router()

LANG_MAP = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇰🇬 Кыргызча": "kg",
}
LOCALES = {"ru": ru.texts, "en": en.texts, "kg": kg.texts}


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Пожалуйста, выберите язык / Please select a language / Тилди тандаңыз:",
        reply_markup=language_kb(),
    )


@router.message(F.text.in_(LANG_MAP))
async def select_language(message: Message, state: FSMContext) -> None:
    lang = LANG_MAP[message.text]
    await state.update_data(lang=lang)
    t = LOCALES[lang]
    await message.answer(t["main_menu"], reply_markup=main_menu_kb(t), parse_mode="HTML")


@router.message(F.text.in_(["🌐 Смена языка", "🌐 Change Language", "🌐 Тилди өзгөртүү"]))
async def change_language(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Пожалуйста, выберите язык / Please select a language / Тилди тандаңыз:",
        reply_markup=language_kb(),
    )


@router.message(F.text.in_(["📜 Правила пользования", "📜 Terms of Use", "📜 Колдонуу эрежелери"]))
async def show_rules(message: Message, t: dict) -> None:
    await message.answer(t["rules"], parse_mode="HTML")


@router.message(F.text.in_(["🎰 Лас Вегас", "🎰 Las Vegas"]))
async def las_vegas(message: Message, t: dict) -> None:
    await message.answer(t["las_vegas_wip"])
