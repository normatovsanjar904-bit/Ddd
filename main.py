import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# O'zingizning Bot Tokeningizni bu yerga qo'ying
API_TOKEN = 'BOT_TOKENINGIZNI_SHU_YERGA_YOZING'
# GitHub'ga yuklagan HTML saytingiz manzilini bu yerga qo'ying
WEB_APP_URL = 'https://username.github.io/repo-nomi/'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Mini App'ni ochadigan tugma
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Do'konni ochish", web_app=WebAppInfo(url=WEB_APP_URL)))
    
    await message.answer(
        f"Assalomu alaykum {message.from_user.first_name}!\n"
        "Bizning onlayn do'konimizga xush kelibsiz. "
        "Pastdagi tugmani bosib savdoni boshlang:", 
        reply_markup=markup
    )

@dp.message_handler(content_types=['web_app_data'])
async def get_web_app_data(message: types.Message):
    # Mini App'dan yuborilgan JSON ma'lumotni qabul qilish
    data = json.loads(message.web_app_data.data)
    
    items_text = "\n".join([f"- {item['name']}: {item['price']} so'm" for item in data['items']])
    
    report = (
        "🛍 **Yangi Buyurtma!**\n\n"
        f"👤 Mijoz: {data['user']}\n"
        f"📦 Mahsulotlar:\n{items_text}\n\n"
        f"💰 Jami: {data['total']} so'm\n"
        f"💳 To'lov turi: {data['payment'].upper()}\n"
    )
    
    # Buyurtmani foydalanuvchiga tasdiqlash va adminga yuborish
    await message.answer(f"Rahmat! Buyurtmangiz qabul qilindi:\n\n{report}")
    # Agar adminga yubormoqchi bo'lsangiz (ID o'rniga o'z IDingizni qo'ying):
    # await bot.send_message(CHAT_ID, report)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
