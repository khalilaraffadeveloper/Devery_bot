# delivery_bot.py
import telebot
from telebot import types
from datetime import datetime
import os  # مهم لقراءة متغيرات البيئة

# === التعديلات الأساسية ===
TOKEN = os.environ['TOKEN']  # سيأتي من إعدادات Render
OWNER_CHAT_ID = os.environ['OWNER_CHAT_ID']  # سيأتي من إعدادات Render
# =========================

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['id'])
def send_my_id(message):
    bot.send_message(message.chat.id,
                     f"معرّف الشات (chat id) الخاص بك هو:\n`{message.chat.id}`",
                     parse_mode='Markdown')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    loc_btn = types.KeyboardButton(text="أرسل موقعي 📍", request_location=True)
    contact_btn = types.KeyboardButton(text="أرسل رقم هاتفي ☎️", request_contact=True)
    markup.add(loc_btn)
    markup.add(contact_btn)
    welcome = ("أهلًا بك أخي الزبون!\n"
           "لإرسال موقعك بسرعة إلى عامل التوصيل،\n"
           "اضغط زر «أرسل موقعي».\n"
           "سيُستخدم الموقع فقط لتوصيل الطلب الآن.")

    bot.send_message(message.chat.id, welcome, reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    user = message.from_user
    username = f"@{user.username}" if user.username else f"{user.first_name or ''}"
    time_received = datetime.fromtimestamp(message.date).strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(message.chat.id, "شكرًا! تم استلام موقعك وسيستخدم فقط لتوصيل طلبك الآن.")
    bot.send_location(OWNER_CHAT_ID, lat, lon)
    maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
    text = (f"📍 موقع زبون جديد\n"
            f"الزائر: {username}\n"
            f"وقت الإرسال: {time_received}\n"
            f"خريطة: {maps_link}")
    bot.send_message(OWNER_CHAT_ID, text)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    info = f"تم استلام رقم: {contact.phone_number} — {contact.first_name}"
    bot.send_message(message.chat.id, "شكرًا! استلمنا رقم هاتفك.")
    bot.send_message(OWNER_CHAT_ID, f"رقم زبون: {contact.phone_number}\nالاسم: {contact.first_name}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
