from aiogram.fsm.state import StatesGroup, State


class AddChannelState(StatesGroup):
    set_link: State = State()
    choosing_name: State = State()
