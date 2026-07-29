import os
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

QR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", "mbank.jpg")

from config import settings
from states.topup import TopupStates
from keyboards.captcha import topup_captcha_kb, TOPUP_CAPTCHA_ANSWER
from keyboards.banks import banks_kb, confirm_id_kb
from keyboards.admin import topup_admin_kb
from keyboards.main import main_menu_kb
from utils.validators import is_valid_xbet_id, is_valid_amount
from utils.order import generate_order_id
from utils.deeplinks import get_bank_url

router = Router()

TOPUP_TRIGGERS = ["💵 Пополнение счета", "💵 Top Up Account", "💵 Эсепти толуктоо"]


@router.message(F.text.in_(TOPUP_TRIGGERS))
async def topup_start(message: Message, state: FSMContext, t: dict) -> None:
    await state.set_state(TopupStates.captcha)
    await message.answer(t["captcha_topup"], reply_markup=topup_captcha_kb())


@router.callback_query(TopupStates.captcha, F.data.startswith("captcha:"))
async def topup_captcha(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    chosen = callback.data.split(":", 1)[1]
    if chosen != TOPUP_CAPTCHA_ANSWER:
        await callback.answer(t["captcha_wrong"], show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=topup_captcha_kb())
        return

    await callback.message.delete()
    await state.set_state(TopupStates.enter_id)
    await callback.message.answer(t["enter_1xbet_id"], parse_mode="HTML")
    await callback.answer()


@router.message(TopupStates.enter_id)
async def topup_enter_id(message: Message, state: FSMContext, t: dict) -> None:
    if not is_valid_xbet_id(message.text or ""):
        await message.answer(t["invalid_id"])
        return

    xbet_id = message.text.strip()
    await state.update_data(xbet_id=xbet_id)
    await state.set_state(TopupStates.confirm_id)
    await message.answer(
        t["confirm_id"].format(id=xbet_id),
        reply_markup=confirm_id_kb(t),
        parse_mode="HTML",
    )


@router.callback_query(TopupStates.confirm_id, F.data == "confirm_id:no")
async def topup_reenter_id(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    await callback.message.delete()
    await state.set_state(TopupStates.enter_id)
    await callback.message.answer(t["enter_1xbet_id"], parse_mode="HTML")
    await callback.answer()


@router.callback_query(TopupStates.confirm_id, F.data == "confirm_id:yes")
async def topup_confirmed_id(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    await callback.message.delete()
    await state.set_state(TopupStates.enter_amount)
    await callback.message.answer(
        t["enter_amount"].format(min=settings.MIN_TOPUP, max=settings.MAX_TOPUP),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(TopupStates.enter_amount)
async def topup_enter_amount(message: Message, state: FSMContext, t: dict) -> None:
    valid, amount = is_valid_amount(message.text or "", settings.MIN_TOPUP, settings.MAX_TOPUP)
    if not valid:
        await message.answer(
            t["invalid_amount"].format(min=settings.MIN_TOPUP, max=settings.MAX_TOPUP)
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(TopupStates.select_bank)
    await message.answer(t["select_bank"], reply_markup=banks_kb(t))


@router.callback_query(TopupStates.select_bank, F.data.startswith("bank:"))
async def topup_select_bank(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    bank = callback.data.split(":", 1)[1]
    data = await state.get_data()
    xbet_id = data["xbet_id"]
    amount = data["amount"]
    order_id = generate_order_id(callback.from_user.id)

    await state.update_data(bank=bank, order_id=order_id)
    await state.set_state(TopupStates.await_receipt)

    bank_url = get_bank_url(bank)
    keyboard = None
    if bank_url:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=t["btn_pay"].format(bank=bank),
                    url=bank_url,
                )
            ]]
        )

    await callback.message.edit_text(
        t["order_created"].format(
            order_id=order_id,
            amount=f"{amount:,}".replace(",", " "),
            bank=bank,
            xbet_id=xbet_id,
        ),
        reply_markup=keyboard,
        parse_mode="HTML",
    )

    if os.path.exists(QR_PATH):
        await callback.message.answer_photo(FSInputFile(QR_PATH))

    await callback.answer()


@router.message(TopupStates.await_receipt, F.photo | F.document)
async def topup_receipt(message: Message, state: FSMContext, t: dict, bot: Bot) -> None:
    data = await state.get_data()
    order_id = data["order_id"]
    xbet_id = data["xbet_id"]
    amount = data["amount"]
    bank = data["bank"]
    user = message.from_user

    await message.answer(
        t["receipt_accepted"].format(order_id=order_id),
        parse_mode="HTML",
    )

    caption = (
        f"📥 <b>ЗАЯВКА НА ПОПОЛНЕНИЕ #{order_id}</b>\n\n"
        f"👤 @{user.username or 'нет'} (<code>{user.id}</code>)\n"
        f"🆔 ID 1xBet: <b>{xbet_id}</b>\n"
        f"💰 Сумма: <b>{amount:,} сом</b>\n"
        f"🏛 Банк: <b>{bank}</b>"
    ).replace(",", " ")

    if message.photo:
        await bot.send_photo(
            settings.ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=caption,
            reply_markup=topup_admin_kb(order_id, user.id),
            parse_mode="HTML",
        )
    else:
        await bot.send_document(
            settings.ADMIN_CHAT_ID,
            document=message.document.file_id,
            caption=caption,
            reply_markup=topup_admin_kb(order_id, user.id),
            parse_mode="HTML",
        )

    await state.clear()
