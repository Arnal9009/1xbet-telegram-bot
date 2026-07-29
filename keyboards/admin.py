from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def topup_admin_kb(order_id: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Подтвердить",
                callback_data=f"admin:topup:approve:{order_id}:{user_id}"
            )],
            [InlineKeyboardButton(
                text="❌ Отклонить: Ошибка ID",
                callback_data=f"admin:topup:reject_id:{order_id}:{user_id}"
            )],
            [InlineKeyboardButton(
                text="❌ Отклонить: Нет оплаты",
                callback_data=f"admin:topup:reject_pay:{order_id}:{user_id}"
            )],
        ]
    )


def withdraw_admin_kb(order_id: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Выплачено",
                callback_data=f"admin:withdraw:approve:{order_id}:{user_id}"
            )],
            [InlineKeyboardButton(
                text="❌ Отклонить: Неверный код",
                callback_data=f"admin:withdraw:reject_code:{order_id}:{user_id}"
            )],
        ]
    )
