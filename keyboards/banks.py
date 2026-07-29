from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BANKS = ["MBank", "Bakai", "Optima Bank", "MegaPay", "Simbank", "DemirBank", "O!Bank"]


def banks_kb() -> InlineKeyboardMarkup:
    rows = []
    for i in range(0, len(BANKS), 2):
        row = [
            InlineKeyboardButton(text=BANKS[i], callback_data=f"bank:{BANKS[i]}")
        ]
        if i + 1 < len(BANKS):
            row.append(InlineKeyboardButton(text=BANKS[i + 1], callback_data=f"bank:{BANKS[i + 1]}"))
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirm_id_kb(t: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t["btn_confirm_yes"], callback_data="confirm_id:yes"),
                InlineKeyboardButton(text=t["btn_confirm_no"], callback_data="confirm_id:no"),
            ]
        ]
    )
