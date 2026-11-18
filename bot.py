import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "9080933145:AAElKH_URsTD1ERmrvXK67GpiXy2eroEGdc"
ADMIN_ID = 7656643763
KASPI_NUMBER = "+77786286359"
KASPI_NAME = "ВСТАВЬ_ИМЯ_КАК_В_KASPI"
MY_NICK = "@Sanek_krg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

CITIES = ["Караганда", "Темиртау", "Шахтинск", "Сарань", "Абай", "Балхаш", "Жезказган", "Каркаралинск", "Осакаровка", "Нура"]
CATEGORIES = ["🛠 Услуги", "🏗 Строительство", "🔥 Сварка", "🚿 Сантехника", "🚗 Авто", "🏠 Недвижимость", "💼 Работа", "🎁 Отдам даром"]
ads_db = []

class AddAd(StatesGroup):
    city = State()
    category = State()
    text = State()
    contact = State()

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подать объявление", callback_data="add")],
        [InlineKeyboardButton(text="🔍 Смотреть объявления", callback_data="view")],
        [InlineKeyboardButton(text="⭐ Поднять / Закрепить", callback_data="promote")],
        [InlineKeyboardButton(text="💼 Реклама в боте", callback_data="reklama")],
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Это *СОСЕД KZ* — доска объявлений Карагандинской области.\n\nКараганда, Темиртау, Шахтинск, Сарань, Балхаш и вся область.\n\nВыбирай, что нужно:", parse_mode="Markdown", reply_markup=main_keyboard())

@dp.callback_query(F.data == "add")
async def add_start(callback: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=c, callback_data=f"city_{c}")] for c in CITIES])
    await callback.message.answer("Выбери город:", reply_markup=kb)
    await state.set_state(AddAd.city)

@dp.callback_query(F.data.startswith("city_"))
async def city_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(city=callback.data.replace("city_", ""))
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=c, callback_data=f"cat_{c}")] for c in CATEGORIES])
    await callback.message.answer("Выбери категорию:", reply_markup=kb)
    await state.set_state(AddAd.category)

@dp.callback_query(F.data.startswith("cat_"))
async def cat_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data.replace("cat_", ""))
    await callback.message.answer("Напиши текст объявления (что предлагаешь, цена):")
    await state.set_state(AddAd.text)

@dp.message(AddAd.text)
async def text_saved(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Теперь отправь свой WhatsApp / Telegram для связи:")
    await state.set_state(AddAd.contact)

@dp.message(AddAd.contact)
async def contact_saved(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ad = f"📍 {data['city']} | {data['category']}\n\n{data['text']}\n\n📞 {message.text}"
    ads_db.append(ad)
    await message.answer(f"✅ Готово! Твое объявление опубликовано:\n\n{ad}", reply_markup=main_keyboard())
    try:
        await bot.send_message(ADMIN_ID, f"🆕 Новое объявление:\n\n{ad}")
    except:
        pass
    await state.clear()

@dp.callback_query(F.data == "view")
async def view_ads(callback: types.CallbackQuery):
    if not ads_db:
        await callback.message.answer("Пока пусто. Стань первым!")
        return
    text = "\n\n---\n\n".join(ads_db[-10:])
    await callback.message.answer(f"📋 Последние объявления:\n\n{text}")

@dp.callback_query(F.data == "promote")
async def promote(callback: types.CallbackQuery):
    await callback.message.answer(f"⭐ Продвижение объявления\n\n1. Закреп на 24ч — 1000 тг\n2. Выделение цветом — 300 тг\n3. Рассылка по каналу — 1500 тг\n\nНапиши мне: {MY_NICK} — договоримся по оплате.")
@dp.callback_query(F.data == "reklama")
async def reklama(callback: types.CallbackQuery):
    await callback.message.answer(f"💼 Реклама в СОСЕД KZ\n\nБаннер — 15 000 тг/мес\nРеклама в боте — 10 000 тг/мес\n\nПиши: {MY_NICK}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())