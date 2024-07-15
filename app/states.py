from aiogram.fsm.state import StatesGroup, State

class ShortLinkFSM(StatesGroup):
    waiting_for_url = State()

class ShortLinkFSM_QR(StatesGroup):
    waiting_for_url_QR = State()

class password_generate(StatesGroup):
    password_length = State()

class weather_check(StatesGroup):
    weather_state = State()

class token_generate(StatesGroup):
    generate_TK = State()

class CURS_VAL(StatesGroup):
    CURS_VAL_one = State()
    CURS_VAL_two = State()
    CURS_VAL_three = State()
    CURS_VAL_four = State()

class STOCK_CHART(StatesGroup):
    STOCK_CHART_one = State()
    STOCK_CHART_two = State()

class READ_TEXT(StatesGroup):
    READ_TEXT_one = State()
    READ_TEXT_two = State()

class QR(StatesGroup):
    qr_code_one = State()
    qr_code_two = State()
    qr_code_three = State()

class TextFromImage(StatesGroup):
    waiting_for_image = State()

class ParseWebsiteStates(StatesGroup):
    website_url = State()
    info_type = State()