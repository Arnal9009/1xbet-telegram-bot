from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import settings
from states.withdraw import WithdrawStates
from keyboards.captcha import withdraw_captcha_kb, WITHDRAW_CAPTCHA_ANSWER
from keyboards.banks import confirm_id_kb
from keyboards.admin import withdraw_admin_kb
from utils.validators import is_valid_xbet_id
from utils.order import generate_order_id

router = Router()

WITHDRAW_TRIGGERS = ["💳 Вывод средств", "💳 Withdraw Funds", "💳 Каражат чыгаруу"]


@router.message(F.text.in_(WITHDRAW_TRIGGERS))
async def withdraw_start(message: Message, state: FSMContext, t: dict) -> None:
    await state.set_state(WithdrawStates.captcha)
    await message.answer(t["captcha_withdraw"], reply_markup=withdraw_captcha_kb())


@router.callback_query(WithdrawStates.captcha, F.data.startswith("captcha:"))
async def withdraw_captcha(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    chosen = callback.data.split(":", 1)[1]
    if chosen != WITHDRAW_CAPTCHA_ANSWER:
        await callback.answer(t["captcha_wrong"], show_alert=True)
        await callback.message.edit_reply_markup(reply_markup=withdraw_captcha_kb())
        return

    await callback.message.delete()
    await state.set_state(WithdrawStates.upload_qr)
    await callback.message.answer(t["upload_qr"], parse_mode="HTML")
    await callback.answer()


@router.message(WithdrawStates.upload_qr, F.photo | F.document)
async def withdraw_upload_qr(message: Message, state: FSMContext, t: dict) -> None:
    if message.photo:
        await state.update_data(qr_file_id=message.photo[-1].file_id, qr_type="photo")
    else:
        await state.update_data(qr_file_id=message.document.file_id, qr_type="document")

    await state.set_state(WithdrawStates.enter_id)
    await message.answer(t["qr_received"] + "\n\n" + t["enter_1xbet_id"], parse_mode="HTML")


@router.message(WithdrawStates.enter_id)
async def withdraw_enter_id(message: Message, state: FSMContext, t: dict) -> None:
    if not is_valid_xbet_id(message.text or ""):
        await message.answer(t["invalid_id"])
        return

    xbet_id = message.text.strip()
    await state.update_data(xbet_id=xbet_id)
    await state.set_state(WithdrawStates.confirm_id)
    await message.answer(
        t["confirm_id"].format(id=xbet_id),
        reply_markup=confirm_id_kb(t),
        parse_mode="HTML",
    )


@router.callback_query(WithdrawStates.confirm_id, F.data == "confirm_id:no")
async def withdraw_reenter_id(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    await callback.message.delete()
    await state.set_state(WithdrawStates.enter_id)
    await callback.message.answer(t["enter_1xbet_id"], parse_mode="HTML")
    await callback.answer()


@router.callback_query(WithdrawStates.confirm_id, F.data == "confirm_id:yes")
async def withdraw_confirmed_id(callback: CallbackQuery, state: FSMContext, t: dict) -> None:
    data = await state.get_data()
    xbet_id = data["xbet_id"]
    await callback.message.delete()
    await state.set_state(WithdrawStates.enter_withdraw_code)
    await callback.message.answer(
        t["withdraw_instruction"].format(id=xbet_id, operator=settings.OPERATOR_USERNAME),
        parse_mode="HTML",
    )
    await callback.message.answer(t["enter_withdraw_code"])
    await callback.answer()


@router.message(WithdrawStates.enter_withdraw_code)
async def withdraw_enter_code(message: Message, state: FSMContext, t: dict, bot: Bot) -> None:
    code = (message.text or "").strip()
    if not code:
        await message.answer(t["enter_withdraw_code"])
        return

    data = await state.get_data()
    xbet_id = data["xbet_id"]
    qr_file_id = data["qr_file_id"]
    qr_type = data["qr_type"]
    order_id = generate_order_id(message.from_user.id)
    user = message.from_user

    await message.answer(t["withdraw_accepted"], parse_mode="HTML")

    caption = (
        f"📤 <b>ЗАЯВКА НА ВЫВОД #{order_id}</b>\n\n"
        f"👤 @{user.username or 'нет'} (<code>{user.id}</code>)\n"
        f"🆔 ID 1xBet: <b>{xbet_id}</b>\n"
        f"🔑 Код вывода: <b>{code}</b>"
    )

    if qr_type == "photo":
        await bot.send_photo(
            settings.ADMIN_CHAT_ID,
            photo=qr_file_id,
            caption=caption,
            reply_markup=withdraw_admin_kb(order_id, user.id),
            parse_mode="HTML",
        )
    else:
        await bot.send_document(
            settings.ADMIN_CHAT_ID,
            document=qr_file_id,
            caption=caption,
            reply_markup=withdraw_admin_kb(order_id, user.id),
            parse_mode="HTML",
        )

    await state.clear()
