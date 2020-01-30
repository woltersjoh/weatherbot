from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import BME280
from SI1145 import SI1145
si1145 = SI1145()

updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher

# bot listeners
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello {} 👋'.format(update.message.from_user.first_name))
    context.bot.send_message(chat_id=update.effective_chat.id, text=selection_message(), reply_markup=selection_keyboard())

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=overview_message())

def handle_message(update, context):
    text = update.message.text
    if text == 'hello':
        context.bot.send_message(chat_id=update.effective_chat.id, text='Hallo {} 👋'.format(update.message.from_user.first_name))

# bot messages
def summary(update, context):
    getTemperature(update, context)
    getHumidity(update, context)
    getPressure(update, context)
    getUltraviolet(update, context)
    getIlluminance(update, context)
    getInfrared(update, context)

def selection(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=selection_message(),
                          reply_markup=first_menu())

def selection_message():
    return 'Was mÃ¶chtest du Ã¼ber das aktuelle Wetter wissen? 🌤'

def overview_message():
    return 'Telegram-Weather-Bot 🌤⛈☀\n Ich kann dich mit den folgenden Kommandos unterstÃ¼tzen:\n\n▪ /start\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tEine Gesamtansicht bekommst du mit:\n▪ /weather\t\t\t\t\t\t\t\tEine Zusammenfassung von deinem aktuellen Wetter.\n\nFür eine Beschreibung des Bots besuche:\n/https://github.com/woltersjoh/weatherbot

# buttons
def getTemperature(update, context):
    temperature = BME280.readTemperature()

    if temperature < 25 and > 5:
        normal = "MÃ¶chtest du mehr über das aktuelle Wetter erfahren? 🙂"
        normal_icon = "⛅"
    elif temperature <= 5:
        cold = "Winterjacke ✔ Schal ✔ Dicke Socken ✔ - Nicht das du dir eine ErkÃ¤ltung holst 🙏"
        cold_icon = "🥶"
    elif temperature >= 25:
        warm = "Oh und vergiss bitte nicht deine Sonnencreme aufzutragen 😎🏝"
        warm_icon = "☀"

    context.bot.send_message(chat_id=update.effective_chat.id, text='Die aktuelle Temepratur liegt %f Â°C' %temperature )
    context.bot.send_message(chat_id=update.effective_chat.id, text='{w.warm}{w.cold}'.format(w=getTemperature()))

def getHumidity(update, context):
    humidity = BME280.readHumidity()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Die Luftfeuchte liegt bei %f Prozent' %humidity )

def getPressure(update, context):
    pressure = BME280.readPressure()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Der Luftdruck liegt bei %f hPa' %pressure )

def getUltraviolet(update, context):
    ultraviolet = si1145.readUV()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Die WellenlÃ¤nge der elektromagnetischen Strahlung liegt bei %f nm' %ultraviolet )

def getIlluminance(update, context):
    illuminance = si1145.readVisible()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Die LichtstÃ¤rke betrÃ¤gt %f lx' %illuminance )

def getInfrared(update, context):
    infrared = si1145.readIR()
    context.bot.send_message(chat_id=update.effective_chat.id, text='Die UV-Strahlung liegt bei %f nm' %infrared)

# keyboard
def selection_keyboard():
    keyboard = [
        [InlineKeyboardButton('Temperatur', callback_data='temperature')],
        [InlineKeyboardButton('Luftfeuchtigkeit', callback_data='humidity')],
        [InlineKeyboardButton('Luftdruck', callback_data='pressure')],
        [InlineKeyboardButton('IR-Strahlung', callback_data='infrared')],
        [InlineKeyboardButton('Beleuchtungsstärke', callback_data='illuminance')],
        [InlineKeyboardButton('UV-Strahlung', callback_data='ultraviolet')]
    ]
    return InlineKeyboardMarkup(keyboard)

# updater
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hilfe', help))
updater.dispatcher.add_handler(CommandHandler('Ã¼berblick', summary))
updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=handle_message))
updater.dispatcher.add_handler(CallbackQueryHandler(temperature_button, pattern='temperature'))
updater.dispatcher.add_handler(CallbackQueryHandler(humidity_button, pattern='humidity'))
updater.dispatcher.add_handler(CallbackQueryHandler(pressure_button, pattern='pressure'))
updater.dispatcher.add_handler(CallbackQueryHandler(infrared_button, pattern='infrared'))
updater.dispatcher.add_handler(CallbackQueryHandler(illuminance_button, pattern='illuminance'))
updater.dispatcher.add_handler(CallbackQueryHandler(ultraviolet_button, pattern='ultraviolet'))

updater.start_polling()
