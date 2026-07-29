from aiogram.fsm.state import State, StatesGroup


class TopupStates(StatesGroup):
    captcha = State()
    enter_id = State()
    confirm_id = State()
    enter_amount = State()
    select_bank = State()
    await_receipt = State()
