from aiogram.fsm.state import StatesGroup, State


class AddChannelState(StatesGroup):
    set_link: State = State()
    set_name: State = State()


class ChangeChannelGeoState(StatesGroup):
    set_name: State = State()
