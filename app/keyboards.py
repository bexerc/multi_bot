from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="узнать курс валют 💸"),
            KeyboardButton(text="график акций 📊"),
        ],
        [
            KeyboardButton(text="узнать курс криптовалют! 💰"),
        ],
        [
            KeyboardButton(text="текст из фотграфии 🖼️"),
        ],
        [
            KeyboardButton(text="короткая ссылка 🔗"),
        ],
        [
            KeyboardButton(text="qr code 📱"),
            KeyboardButton(text="ссылка из QR 📱"),
            KeyboardButton(text="парсинг сайта🤖"),
        ],
        [
            KeyboardButton(text="генератор пароля 🔒"),
            KeyboardButton(text="генерация токена 🔑"),
        ],
        [
            KeyboardButton(text="узнать погоду ☁️"),
        ],
        [
            KeyboardButton(text="озвучка 🗣️"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите действие снизу",

)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌cancel❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите действие снизу",
    selective=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="да"),
        ],
        [
            KeyboardButton(text="нет"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите действие снизу",
    selective=True
)

currency_KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇦🇺 AUD"),
            KeyboardButton(text="🇦🇿 AZN"),
            KeyboardButton(text="🇬🇧 GBP"),
        ],
        [
            KeyboardButton(text="🇦🇲 AMD"),
            KeyboardButton(text="🇧🇾 BYN"),
            KeyboardButton(text="🇧🇬 BGN"),
        ],
        [
            KeyboardButton(text="🇧🇷 BRL"),
            KeyboardButton(text="🇭🇺 HUF"),
            KeyboardButton(text="🇭🇰 HKD"),
        ],
        [
            KeyboardButton(text="🇩🇰 DKK"),
            KeyboardButton(text="🇺🇸 USD"),
            KeyboardButton(text="🇪🇺 EUR"),
        ],
        [
            KeyboardButton(text="🇮🇳 INR"),
            KeyboardButton(text="🇰🇿 KZT"),
            KeyboardButton(text="🇨🇦 CAD"),
        ],
        [
            KeyboardButton(text="🇰🇬 KGS"),
            KeyboardButton(text="🇨🇳 CNY"),
            KeyboardButton(text="🇰🇷 KRW"),
        ],
        [
            KeyboardButton(text="🇲🇩 MDL"),
            KeyboardButton(text="🇳🇴 NOK"),
            KeyboardButton(text="🇵🇱 PLN"),
        ],
        [
            KeyboardButton(text="🇷🇴 RON"),
            KeyboardButton(text="🇸🇩 XDR"),
            KeyboardButton(text="🇸🇬 SGD"),
        ],
        [
            KeyboardButton(text="🇹🇯 TJS"),
            KeyboardButton(text="🇹🇷 TRY"),
            KeyboardButton(text="🇹🇲 TMT"),
        ],
        [
            KeyboardButton(text="🇺🇿 UZS"),
            KeyboardButton(text="🇺🇦 UAH"),
            KeyboardButton(text="🇨🇿 CZK"),
        ],
        [
            KeyboardButton(text="🇸🇪 SEK"),
            KeyboardButton(text="🇨🇭 CHF"),
            KeyboardButton(text="🇯🇵 JPY"),
        ],
        [
            KeyboardButton(text="❌cancel❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите валюту",
    selective=True
)

currency_KB_GR = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇸 USD"),
            KeyboardButton(text="🇪🇺 EUR"),
        ],
        [
            KeyboardButton(text="🇷🇺 RUB"),
            KeyboardButton(text="🇬🇧 GBP"),
        ],
        [
            KeyboardButton(text="❌cancel❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите валюту",
    selective=True
)


language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Русский"),
        ],
        [
            KeyboardButton(text="Английский"),
        ],
        [
            KeyboardButton(text="Французский"),
        ],
        [
            KeyboardButton(text="❌cancel❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите действие снизу",
    selective=True
)

pars = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="заголовок"),
            KeyboardButton(text="текст"),
            KeyboardButton(text="ссылки"),
        ],
        [
            KeyboardButton(text="изображения"),
        ],
        [
            KeyboardButton(text="❌cancel❌"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="выберите действие снизу",
    selective=True
)

kontacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="НАПИСАТЬ",url="https://t.me/dszzfn")]
])


stock_kb= InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="AAPL 🍎", callback_data="AAPL 🍎"),InlineKeyboardButton(text="GOOG 🤖", callback_data="GOOG 🤖")],
    [InlineKeyboardButton(text="MSFT 📊", callback_data="MSFT 📊")],
    [InlineKeyboardButton(text="❌cancel❌", callback_data="❌cancel❌")]
])