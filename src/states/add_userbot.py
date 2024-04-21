from aiogram.fsm.state import StatesGroup, State


class AddUserbotState(StatesGroup):
    phone: State = State()
    code: State = State()
