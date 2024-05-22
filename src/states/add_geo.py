from aiogram.fsm.state import StatesGroup, State


class AddGeoState(StatesGroup):
    set_name: State = State()
