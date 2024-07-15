import os
import html
import pycbrf
import aiohttp
import asyncio
import random
import secrets
import qrcode
import pyshorteners
import urllib.parse
from PIL import Image
from twilio.rest import Client
import pytesseract
import pyzbar.pyzbar as pyzbar
from gtts import gTTS
import yfinance as yf
from io import BytesIO
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from os import getenv
from dotenv import load_dotenv
from pyshorteners.exceptions import ShorteningErrorException


from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery
from states import (
    ShortLinkFSM,
    ShortLinkFSM_QR,
    password_generate,
    weather_check,
    token_generate,
    CURS_VAL,
    STOCK_CHART,
    READ_TEXT,
    QR,
    TextFromImage,
    ParseWebsiteStates
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart


import app.keyboards as kb

router = Router()



@router.message(CommandStart())
async def reg_one(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Я - Telegram-бот \"MULT\".\n"
        "Я готов помочь вам в повседневной жизни и работе. Мои возможности:\n"
        "💸 Актуальные курсы валют\n"
        "📊 Графики изменения цен на акции\n"
        "💰 Курсы популярных криптовалют\n"
        "🔗 Короткие ссылки из длинных URL\n"
        "🔒 Надежные пароли\n"
        "🔑 Уникальные токены\n"
        "☁️ Прогноз погоды\n"
        "🗣️ Озвучивание текста на 3 языках\n"
        "Напишите мне, и я помогу вам решить любые задачи!",
        reply_markup=kb.main
    )
    
@router.message(F.text == "❌cancel❌")
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("вы вышли в главное меню", reply_markup=kb.main)
    
@router.callback_query(F.text == "❌cancel❌")
async def cancel_handler(message: Message, state: FSMContext,callback: CallbackQuery):
    await state.clear()
    await callback.answer("вы вышли в главное меню", reply_markup=kb.main)
    
    

@router.message(F.text == '/restart')
async def restart_bot(message: Message, state: FSMContext):
    await state.set_state(None)  # reset the state to None
    await state.update_data({})  # clear the state data
    await reg_one(message)  # call the start command handler again

@router.message(F.text == '/help')
async def menu(message:Message):
    await message.answer(f'{message.from_user.first_name},если у вас возникли проблемы с ботом напишите нам',parse_mode='HTML',reply_markup=kb.kontacts)

@router.message(F.text == '/start')
async def restart_bot(message: Message, state: FSMContext):
    await state.set_state(None)  # reset the state to None
    await state.update_data({})  # clear the state data
    await reg_one(message)
    
    
@router.message(F.text == "узнать курс криптовалют! 💰")
async def get_currency_rates(message: Message):
    async with aiohttp.ClientSession() as session:
        API_CRIPT = getenv('API_CRIPT')
        async with session.get(API_CRIPT) as response:
            data = await response.json()
            coins = data['coins']
            table = PrettyTable(['name', 'Symbol',
                                 'Market Cap Rank',
                                 'Price', 'Price Change (24h)'])
            for coin in coins:
                table.add_row([
                    coin['item']['name'],
                    coin['item']['symbol'],
                    coin['item']['market_cap_rank'],
                    coin['item']['data']['price'],
                    f"{coin['item']['data']['price_change_percentage_24h']['usd']}%"
                ])
            code = (f"```\n{table}\n```")
            await message.reply(f"{code}", parse_mode='Markdown', reply_markup=kb.main)
    

@router.message(F.text == 'короткая ссылка 🔗')
async def start_command(message: Message, state: FSMContext):
    await state.set_state(ShortLinkFSM.waiting_for_url)
    await message.answer("пришлите мне свою ссылку", reply_markup=kb.cancel)


@router.message(ShortLinkFSM.waiting_for_url)
async def get_url(message: Message, state: FSMContext):
    url = message.text
    if url.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в главное меню", reply_markup=kb.main)
    if not url.startswith('http://') and not url.startswith('https://'):
        await message.reply("Вы не прислали ссылку. Пожалуйста, пришлите мне ссылку в формате http:// или https://")
        await state.clear()
    await state.update_data(waiting_for_url=url)
    await message.answer("обработка ссылки...", reply_markup=kb.main)
    pys = pyshorteners.Shortener()
    try:
        short_link = pys.tinyurl.short(url)
        await message.reply(f"Вот укороченная ссылка:{short_link}",reply_markup=kb.main)
        await state.clear()
    except ShorteningErrorException as e:
        await message.reply(f"Ошибка укорачивания ссылки",reply_markup=kb.main)
        print(e)
        await state.clear()
            
@router.message(F.text == 'qr code 📱')
async def start_command(message: Message, state: FSMContext):
    await state.set_state(ShortLinkFSM_QR.waiting_for_url_QR)
    await message.answer("пришлите мне свою ссылку и из нее я сделаю qr code", reply_markup=kb.cancel)

@router.message(ShortLinkFSM_QR.waiting_for_url_QR)
async def get_url(message: Message, state: FSMContext):
    await state.update_data(waiting_for_url_QR = message.text)
    if message.text.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("генерация отменена", reply_markup=kb.main)
    await message.answer("обработка ссылки...")
    data = await state.get_data()
    url= data['waiting_for_url_QR']
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = f"qrcode_{message.from_user.id}.png"
    img.save(img_path)
    photo = FSInputFile(path=f"qrcode_{message.from_user.id}.png")
    await message.answer_photo(photo, caption="<b><u> вот Qr code из вашей ссылки </u></b>", parse_mode='HTML', reply_markup=kb.main)
    os.remove(img_path)
    await state.clear()
    
    
@router.message(F.text == 'генерация токена 🔑')
async def start_command(message: Message, state: FSMContext):
    await state.set_state(token_generate.generate_TK)
    await message.answer("пришлите мне желаемую длинну токена и я сгенерирую вам пароль", reply_markup=kb.cancel)
    
@router.message(token_generate.generate_TK)
async def get_url(message: Message, state: FSMContext):
    if message.text.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("генерация отменена", reply_markup=kb.main)
        return
    try:
        length = int(message.text)
        if length <= 0:
            await message.answer("длина токена должна быть положительной")
            return
    except ValueError:
        await message.answer("я вас не понимаю. Пожалуйста, введите целое положительное число")
        
    await state.update_data(password_length=length)
    msg = await message.answer("ваш токен генерируеться [          ] 0%")
    cancel = False
    for i in range(101):
        if message.text.strip() == "❌cancel❌":
            cancel = True
            break
        
        await asyncio.sleep(0.05)
        progress_bar = "[" + "#" * (i // 10) + " " * (10 - i // 10) + "] " + str(i) + "%"
        if i % 10 == 0:  # edit message only every 10%
            if i != 0:  # don't edit message at 0%
                await msg.edit_text("ваш токен генерируеться " + progress_bar, parse_mode='HTML', disable_notification=True)
                
    if cancel:
        await msg.edit_text("отменено.", parse_mode='HTML', disable_notification=True)
        await state.clear()
    else:
        data = await state.get_data()
        length = data.get('password_length', 0)
        token = secrets.token_urlsafe(length)
        await msg.edit_text(f"ваш токен:\n<code>{html.escape(token)}</code>", parse_mode='HTML', reply_markup=kb.main)
        await state.clear()  # Clear the state
         
@router.message(F.text == 'генератор пароля 🔒')
async def start_command(message: Message, state: FSMContext):
    await state.set_state(password_generate.password_length)
    await message.answer("пришлите мне желаемую длинну пароля и я сгенерирую вам пароль", reply_markup=kb.cancel)
    
@router.message(password_generate.password_length)
async def get_url(message: Message, state: FSMContext):
    if message.text.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в галвное ", reply_markup=kb.main)
    try:
        length = int(message.text)
        if length <= 0:
            await message.answer("длина пароля должна быть положительной")
    except ValueError:
        await message.answer("я вас не понимаю. Пожалуйста, введите целое положительное число")

    await state.update_data(password_length=length)
    
    data = await state.get_data()
    length = data.get('password_length', 0)
    chars = '+-/*!&$?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(int(length)):
        password += random.choice(chars)
    await message.answer(f"ваш пароль:\n<code>{html.escape(password)}</code>", parse_mode='HTML', reply_markup=kb.main)
    await state.clear()
        
        
@router.message(F.text == 'узнать погоду ☁️')
async def start_command(message: Message, state: FSMContext):
    await state.set_state(weather_check.weather_state)
    await message.answer("пришлите мне город погоду которого хотите узнать", reply_markup=kb.cancel)
@router.message(weather_check.weather_state)
async def get_url(message: Message, state: FSMContext):
    citi = message.text
    if citi.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в главное меню",reply_markup=kb.main )
        return
    await state.update_data(weather_state=citi)


    async with aiohttp.ClientSession() as session:
        API_WEATHER = getenv('API_WEATHER')
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={citi}&appid={API_WEATHER}&units=metric&lang=ru') as response:
            data = await response.json()
            if response.status == 404:
                await message.answer("Извините, у меня нет информации по тому городу который вы прислали",reply_markup=kb.main)
                return

    main = data['main']
    weather_description = data['weather'][0]['description']
    temperature = main['temp']
    feels_like = main['feels_like']
    pressure = main['pressure']
    humidity = main['humidity']
    wind = data['wind']['speed']

    weather_text = (f'<b>{citi.upper()}</b>\n'
                    f'{weather_description}\n'
                    f'(температура: {temperature}°C \nпо ощущениям {feels_like}°C)\n'
                    f'Давление: {pressure} hPa\n'
                    f'Влажность: {humidity}%\n'
                    f'Ветер: {wind} m/s')

    await message.answer(f'<b><u>{weather_text}</u></b>', parse_mode='HTML',reply_markup=kb.main)
    await state.clear() 

currencies = {
    '🇦🇺 AUD': 'Австралийский доллар',
    '🇦🇿 AZN': 'Азербайджанский манат', 
    '🇬🇧 GBP': 'Британский фунт',
    '🇦🇲 AMD': 'Армянский драм',
    '🇧🇾 BYN': 'Белорусский рубль',
    '🇧🇬 BGN': 'Болгарский лев',
    '🇧🇷 BRL': 'Бразильский реал',
    '🇭🇺 HUF': 'Венгерский форинт',
    '🇭🇰 HKD': 'Гонконгский доллар',
    '🇩🇰 DKK': 'Датская крона',
    '🇺🇸 USD': 'Доллар США',
    '🇪🇺 EUR': 'Евро',
    '🇮🇳 INR': 'Индийская рупия',
    '🇰🇿 KZT': 'Казахстанский тенге',
    '🇨🇦 CAD': 'Канадский доллар',
    '🇰🇬 KGS': 'Киргизский сом',
    '🇨🇳 CNY': 'Китайский юань',
    '🇰🇷 KRW': 'Корейская вона',
    '🇲🇩 MDL': 'Молдавский лей',
    '🇳🇴 NOK': 'Норвежская крона',
    '🇵🇱 PLN': 'Польский злотый',
    '🇷🇴 RON': 'Румынский лей',
    '🇸🇩 XDR': 'Специальные права заимствования',
    '🇸🇬 SGD': 'Сингапурский доллар',
    '🇹🇯 TJS': 'Таджикский сомони',
    '🇹🇷 TRY': 'Турецкая лира',
    '🇹🇲 TMT': 'Туркменский манат',
    '🇺🇿 UZS': 'Узбекский сум',
    '🇺🇦 UAH': 'Украинская гривна',
    '🇨🇿 CZK': 'Чешская крона',
    '🇸🇪 SEK': 'Шведская крона',
    '🇨🇭 CHF': 'Швейцарский франк',
    '🇯🇵 JPY': 'Японская иена'
}

@router.message(F.text == 'узнать курс валют 💸')
async def get_exchange_rate(message: Message, state: FSMContext):
    await state.set_state(CURS_VAL.CURS_VAL_one)
    cbrf = pycbrf.ExchangeRates()
    
    table = PrettyTable(['Валюта', 'Курс'])
    for code, name in currencies.items():
        code_short = code.split(' ')[1]  # Extract the currency code (e.g. AUD, USD, etc.)
        try:
            rate = cbrf[code_short].value
            table.add_row([f"{name} ({code})", f"{rate:.2f} RUB"])
        except AttributeError:
            table.add_row([f"{name} ({code})", "Нет курса"])
    
    code = (f"```\n{table}\n```")
    await message.answer(code, parse_mode='Markdown')
    
    await message.answer("Хотите посчитать валюту?", reply_markup=kb.yes_no)

@router.message(F.text == 'нет')
async def cancel_currency(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вышли из режима валют", reply_markup=kb.main)

@router.message(F.text == 'да')
async def calculate_currency(message: Message, state: FSMContext):
    await state.set_state(CURS_VAL.CURS_VAL_two)
    await message.answer("Какую валюту будем конвертировать? (напишите имя валюты или 3-х буквенный код)",reply_markup=kb.currency_KB)

@router.message(CURS_VAL.CURS_VAL_two)
async def get_currency_name(message: Message, state: FSMContext):
    currency_input = message.text
    if currency_input.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в главное меню",reply_markup=kb.main )
        return
    for code, name in currencies.items():
        if code.split()[1] == currency_input.upper() or name.lower() == currency_input.lower():
            currency_name = name
            currency_code = code.split()[1]
            break
        elif code.startswith(currency_input):
            currency_name = name
            currency_code = code.split()[1]
            break
    else:
        await message.answer("Валюта не найдена. Попробуйте снова.", reply_markup=kb.currency_KB)
        return
    
    await state.update_data(currency_name=currency_name, currency_code=currency_code)
    await message.answer("Сколько единиц валюты вы хотите конвертировать?")
    await state.set_state(CURS_VAL.CURS_VAL_three)

@router.message(CURS_VAL.CURS_VAL_three)
async def get_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    await state.update_data(amount=amount)
    await message.answer("В какую валюту вы хотите конвертировать? (напишите имя валюты или 3-х буквенный код)")
    await state.set_state(CURS_VAL.CURS_VAL_four)

@router.message(CURS_VAL.CURS_VAL_four)
async def get_target_currency(message: Message, state: FSMContext):
    target_currency_input = message.text
    for code, name in currencies.items():
        if code.split()[1] == target_currency_input.upper() or name.lower() == target_currency_input.lower():
            target_currency_name = name
            target_currency_code = code.split()[1]
            break
        elif code.startswith(target_currency_input):
            target_currency_name = name
            target_currency_code = code.split()[1]
            break
    else:
        await message.answer("Валюта не найдена. Попробуйте снова.", reply_markup=kb.currency_KB)
        return
    
    data = await state.get_data()
    currency_name = data['currency_name']
    amount = data['amount']
    cbrf = pycbrf.ExchangeRates()
    rate = cbrf[data['currency_code']].value
    target_rate = cbrf[target_currency_code].value
    result = amount * float(rate) / float(target_rate)
    await message.answer(f"{amount} {currency_name} = {result:.2f} {target_currency_name}", reply_markup=kb.main)
    await state.clear()
    
    
@router.message(F.text == 'график акций 📊')
async def get_stock_chart(message: Message, state: FSMContext):
    await state.set_state(STOCK_CHART.STOCK_CHART_one)
    await message.answer("Введите тикер компании (например, AAPL для Apple) 📊", reply_markup=kb.stock_kb)

@router.callback_query(STOCK_CHART.STOCK_CHART_one)
async def get_stock_ticker(callback: CallbackQuery, state: FSMContext):
    ticker = callback.data
    if ticker == '❌cancel❌':
        await state.clear()
        await callback.answer("вы вышли в главное меню", reply_markup=kb.main)
        return
    await state.update_data(ticker=ticker)
    await callback.message.answer("Выберите валюту для графика:", reply_markup=kb.currency_KB_GR)
    await state.set_state(STOCK_CHART.STOCK_CHART_two)
    

@router.message(STOCK_CHART.STOCK_CHART_two)
async def get_currency(message: Message, state: FSMContext):
    currency = message.text
    if currency not in ["🇺🇸 USD", "🇪🇺 EUR", "🇷🇺 RUB", "🇬🇧 GBP"]:
        await message.answer("Ошибка: неверная валюта. Пожалуйста, выберите из списка.")
        return
    ticker = (await state.get_data())["ticker"]
    try:
        data = yf.download(ticker, period="1y")
        if data.empty:
            await message.answer("Ошибка: данные акций не доступны для указанного тикера 😔", reply_markup=kb.main)
            await state.clear()
        data['Close'] = data['Close'].apply(lambda x: x * currency_exchange_rate(currency))  # Convert to selected currency
        plt.figure(figsize=(10, 6))
        plt.plot(data.index, data['Close'])
        plt.title(f"{ticker} Stock Price ({currency})")
        plt.xlabel("Date")
        plt.ylabel(f"Price ({currency})")
        plt.grid(True)
        file_name = f"{message.from_user.first_name}"
        plt.savefig(f"{file_name}.png")
        work_schedule = FSInputFile(path=f"{file_name}.png")
        await message.answer_photo(work_schedule, caption=f"<b><u> график акций {ticker} ({currency})</u></b> 📈", parse_mode='HTML', reply_markup=kb.main)
        # Delete the file after sending it to the user
        os.remove(f"{file_name}.png")
        await state.clear()
    except Exception as e:
        await message.answer("Ошибка: не удалось загрузить данные акций 😕", reply_markup=kb.main)
        await state.clear()

def currency_exchange_rate(currency: str) -> float:
    # Implement your currency exchange rate logic here
    # For example, you can use an API or a fixed exchange rate
    exchange_rates = {"🇺🇸 USD": 1, "🇪🇺 EUR": 0.88, "🇷🇺 RUB": 74.12, "🇬🇧 GBP": 0.76}
    return exchange_rates[currency]

@router.message(F.text == 'озвучка 🗣️')
async def read_text(message: Message, state: FSMContext):
    await state.set_state(READ_TEXT.READ_TEXT_one)
    await message.answer("Выберите язык озвучки:", reply_markup=kb.language)

@router.message(READ_TEXT.READ_TEXT_one)
async def choose_language(message: Message, state: FSMContext):
    language = message.text
    if language.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в главное меню",reply_markup=kb.main )
        return
    if language == "Русский":
        language_code = "ru"
    elif language == "Английский":
        language_code = "en"
    elif language == "Французский":
        language_code = "fr"
    else:
        await message.answer("Неправильный выбор языка. Попробуйте снова.", reply_markup=kb.main)
        await state.clear()
        return
    await state.update_data(language_code=language_code)
    await message.answer("Пришлите мне текст, который необходимо озвучить 📝",reply_markup=kb.cancel)
    await state.set_state(READ_TEXT.READ_TEXT_two)

@router.message(READ_TEXT.READ_TEXT_two)
async def get_text_to_read(message: Message, state: FSMContext):
    text = message.text
    if text.strip() == "❌cancel❌":
        await state.clear()
        await message.answer("вы вышли в главное меню",reply_markup=kb.main )
        return
    language_code = (await state.get_data())["language_code"]
    user_id = message.from_user.id
    file_name = f"{user_id}.mp3"
    tts = gTTS(text=text, lang=language_code)
    tts.save(file_name)
    with open(file_name, "rb") as audio:
        work_schedule = FSInputFile(path=file_name)
        await message.answer_audio(work_schedule,reply_markup=kb.main)
    os.remove(file_name)  # Remove the audio file after sending it
    await state.clear()


@router.message(F.text == 'ссылка из QR 📱')
async def process_qr_code_data(message: Message, state: FSMContext):
    await message.answer('пришлите фото', reply_markup=kb.cancel)
    await state.set_state(QR.qr_code_one)

@router.message(QR.qr_code_one)
async def process_qr_code_data(message: Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        async with aiohttp.ClientSession() as session:
            TOKEN = getenv('TOKEN')
            async with session.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}") as response:
                file_path = (await response.json())['result']['file_path']
                async with session.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}") as response:
                    image_data = await response.read()
                    image = BytesIO(image_data)
                    image = Image.open(image)
                    decoded_objects = pyzbar.decode(image)
                    if decoded_objects:
                        qr_code_data = decoded_objects[0].data.decode("utf-8")
                        await state.update_data(qr_code_one=qr_code_data)
                        await message.answer(f'QR-код содержит ссылку: {qr_code_data}', reply_markup=kb.main)
                        await state.clear() 
                    else:
                        await message.answer('Не удалось прочитать QR-код', reply_markup=kb.main)
                        await state.clear() 
    elif message.text == '❌cancel❌':
        await state.clear()
        await message.answer('Вы вышли в главное меню', reply_markup=kb.main)
    else:
        await message.answer('Пожалуйста, пришлите фото QR-кода или нажмите ❌cancel❌ для отмены', reply_markup=kb.cancel)
        
@router.message(F.text == 'текст из фотграфии 🖼️')
async def process_qr_code_data(message: Message, state: FSMContext):
    await message.answer('пришлите фото', reply_markup=kb.cancel)
    await state.set_state(TextFromImage.waiting_for_image)

@router.message(TextFromImage.waiting_for_image)
async def process_image(message: Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[-1].file_id
        async with aiohttp.ClientSession() as session:
            TOKEN = getenv('TOKEN')
            async with session.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}") as response:
                file_path = (await response.json())['result']['file_path']
                async with session.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}") as response:
                    image_data = await response.read()
                    image = BytesIO(image_data)
                    image = Image.open(image)
                    # Specify the path to the Tesseract executable
                    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                    # Specify the languages to support (e.g., Russian, English, etc.)
                    languages = ['rus', 'eng', 'fra', 'pa', 'deu', 'ita']  # Add more languages as needed
                    text = ''
                    for lang in languages:
                        try:
                            recognized_text = pytesseract.image_to_string(image, lang=lang)
                            if recognized_text:
                                text += f"**{lang.upper()}**: {recognized_text}\n"
                        except pytesseract.TesseractError:
                            pass
                    if text:
                        await message.answer(f'Распознанный текст:\n{text}', reply_markup=kb.main)
                        await state.clear()
                    else:
                        await message.answer('Не удалось распознать текст на изображении 🤔', reply_markup=kb.main)
                        await state.clear()
    elif message.text == '❌cancel❌':
        await state.clear()
        await message.answer('Вы вышли в главное меню', reply_markup=kb.main)
    else:
        await message.answer('Пожалуйста, пришлите фото с текстом 📷')
    

@router.message(F.text == "парсинг сайта🤖")
async def start(message: Message, state: FSMContext):
    if message.text == '❌cancel❌':
        await state.clear()
        await message.answer('Вы вышли в главное меню', reply_markup=kb.main)
    else:
        await message.answer('Привет! Я могу помочь вам спарсить сайты. Какой сайт вы хотите спарсить?')
        await state.set_state(ParseWebsiteStates.website_url)

@router.message(ParseWebsiteStates.website_url)
async def get_website_url(message: Message, state: FSMContext):
    if message.text == '❌cancel❌':
        await state.clear()
        await message.answer('Вы вышли в главное меню', reply_markup=kb.main)
    else:
        website_url = message.text
        await state.update_data(website_url=website_url)
        await message.answer('Какую информацию вы хотите получить с этого сайта? (например, заголовок, текст, ссылки)', reply_markup=kb.pars)
        await state.set_state(ParseWebsiteStates.info_type)

@router.message(ParseWebsiteStates.info_type)
async def get_info_type(message: Message, state: FSMContext):
    if message.text == 'cancel':
        await state.clear()
        await message.answer('Вы вышли в главное меню', reply_markup=kb.main)
    else:
        info_type = message.text
        data = await state.get_data()
        website_url = data['website_url']
        async with aiohttp.ClientSession() as session:
            async with session.get(website_url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                if info_type == 'заголовок':
                    title = soup.title.string
                    await message.answer(f'Заголовок: {title}', reply_markup=kb.main)
                    await state.clear()
                elif info_type == 'текст':
                    text = soup.get_text()
                    chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
                    for chunk in chunks:
                        if len(chunk) > 4000:  # split into smaller chunks if necessary
                            sub_chunks = [chunk[i:i+2000] for i in range(0, len(chunk), 2000)]
                            for sub_chunk in sub_chunks:
                                await message.answer(f'Текст: {sub_chunk}', reply_markup=kb.main)
                                await asyncio.sleep(1)  # add a 1-second delay between messages
                                await state.clear()
                        else:
                            await message.answer(f'Текст: {chunk}', reply_markup=kb.main)
                            await asyncio.sleep(1)  # add a 1-second delay between messages
                            await state.clear()
                    await state.clear()
                elif info_type == 'ссылки':
                    links = [a['href'] for a in soup.find_all('a', href=True)]
                    working_links = []
                    for link in links:
                        if not link.startswith('http'):
                            link = f'http://{link}'
                        try:
                            async with session.head(link) as response:
                                if response.status == 200:
                                    working_links.append(link)
                        except aiohttp.ClientError:
                            pass
                    formatted_links = '\n'.join([f'• [{link}]({urllib.parse.quote(link, safe=":/")})' for link in working_links])
                    chunks = [formatted_links[i:i+4096] for i in range(0, len(formatted_links), 4096)]
                    for chunk in chunks:
                        if len(chunk) > 4000:  # split into smaller chunks if necessary
                            sub_chunks = [chunk[i:i+2000] for i in range(0, len(chunk), 2000)]
                            for sub_chunk in sub_chunks:
                                await message.answer(f'Ссылки:\n{sub_chunk}', parse_mode='Markdown', reply_markup=kb.main)
                                await asyncio.sleep(1)  # add a 1-second delay between messages
                        else:
                            await message.answer(f'Ссылки:\n{chunk}', parse_mode='Markdown', reply_markup=kb.main)
                            await asyncio.sleep(1)  # add a 1-second delay between messages
                    await state.clear()
                elif info_type == 'изображения':
                    images = [img['src'] for img in soup.find_all('img', src=True)]
                    for image in images:
                        if not image.startswith('http'):
                            image = f'http://{website_url}/{image}'
                        await message.answer(f'Изображение: {image}', reply_markup=kb.main)
                        await asyncio.sleep(1)  # add a 1-second delay between messages
                    await state.clear()
                else:
                    await message.answer('Неверный тип информации. Пожалуйста, попробуйте снова.')
                    await state.clear()
        await state.clear()
        
        

    

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @router.message(F.text == 'скачать видео')
# async def start_command(message: Message, state: FSMContext):
#     await state.set_state(url_check.save_video_state)
#     await message.answer("пришлите мне ссылку на видео ролик который вы хотите скачать")
    

        
        
        
# @router.message(url_check.save_video_state)
# async def get_url(message: types.Message, state: FSMContext):
#     link = message.text
#     await state.update_data(save_video_state=link)
#     yt = mps.Youtube(url=link)
#     stream = yt.streams.filter(only_audio=False).first()
#     filename = stream.default_filename
#     stream.download(output_path="D:\multi_bot\\videos")
#     await message.answer("Video downloaded successfully!")
#     await message.answer_video( filename, caption="Here is your video!")
#     os.remove(filename)
#     await state.finish()
    
#     if message.text.startswith('https://www.youtube.com/'):
#     yt_url = message.text
#     yt = YouTube(yt_url)
#     stream = yt.streams.filter(only_audio=False).first()  # изменено на only_audio=False
#     file_path = stream.download(output_path='videos', filename_prefix='video_')  # добавлено filename_prefix
#     fs_input_file = FSInputFile(file_path)

#     await message.answer_video(open(f'{fs_input_file}', 'rb'))



# @router.message(url_check.save_video_state)
# async def get_url(message: Message, state: FSMContext):
#     if message.text.startswith('https://www.youtube.com/'):
#         yt_url = message.text
#         await state.update_data(save_video_state=yt_url)
#         yt = YouTube(yt_url)
#         stream = yt.streams.filter(only_audio=False).first()  # изменено на only_audio=False
#         file_path = stream.download(output_path='videos', filename_prefix='video_')  # добавлено filename_prefix
#         fs_input_file = FSInputFile(file_path)

#         await message.answer_video( fs_input_file, caption="Here is your video!")
#         os.remove(file_path)
#         await state.finish()
        

