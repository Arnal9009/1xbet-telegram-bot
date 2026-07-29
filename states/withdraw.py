from aiogram.fsm.state import State, StatesGroup


class WithdrawStates(StatesGroup):
    captcha = State()
    upload_qr = State()
    enter_id = State()
    confirm_id = State()
    enter_withdraw_code = State()
