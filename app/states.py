from aiogram.fsm.state import State, StatesGroup


class AddEvent(StatesGroup):
    name = State()
    description = State()
    users_count = State()
    photo = State()
    document = State()

    new_name = State()
    new_description = State()
    new_users_count = State()
    new_photo = State()
    new_document = State()


class Register(StatesGroup):
    full_name = State()
    date_age = State()
    rider_exp = State()
    skate = State()
    helmet = State()
    defender = State()
    parents_name = State()
    parents_contact = State()
    email = State()


class Reject(StatesGroup):
    reason = State()