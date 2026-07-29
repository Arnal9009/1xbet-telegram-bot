from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from locales import ru

router = Router()

# Тексты уведомлений всегда на русском — оператор работает на русском
_t = ru.texts


@router.callback_query(F.data.startswith("admin:topup:"))
async def handle_topup_decision(callback: CallbackQuery, bot: Bot) -> None:
    parts = callback.data.split(":")
    # admin:topup:<action>:<order_id>:<user_id>
    action = parts[2]
    order_id = parts[3]
    user_id = int(parts[4])

    if action == "approve":
        text = _t["topup_approved"]
    elif action == "reject_id":
        text = _t["topup_rejected_wrong_id"]
    else:
        text = _t["topup_rejected_no_payment"]

    await bot.send_message(user_id, text)
    await callback.message.edit_reply_markup(reply_markup=None)
    status_label = "✅ Подтверждено" if action == "approve" else "❌ Отклонено"
    await callback.message.edit_caption(
        caption=callback.message.caption + f"\n\n{status_label} оператором @{callback.from_user.username}",
        parse_mode="HTML",
    )
    await callback.answer("Готово")


@router.callback_query(F.data.startswith("admin:withdraw:"))
async def handle_withdraw_decision(callback: CallbackQuery, bot: Bot) -> None:
    parts = callback.data.split(":")
    # admin:withdraw:<action>:<order_id>:<user_id>
    action = parts[2]
    user_id = int(parts[4])

    if action == "approve":
        text = _t["withdraw_approved"]
    else:
        text = _t["withdraw_rejected_wrong_code"]

    await bot.send_message(user_id, text)
    await callback.message.edit_reply_markup(reply_markup=None)
    status_label = "✅ Выплачено" if action == "approve" else "❌ Отклонено"
    await callback.message.edit_caption(
        caption=callback.message.caption + f"\n\n{status_label} оператором @{callback.from_user.username}",
        parse_mode="HTML",
    )
    await callback.answer("Готово")
