from rozlink import app, db
from rozlink.models import User
import telebot
from telebot import types
import requests
import json
import random
import time

bot = telebot.TeleBot(app.config["TELEGRAM_TOKEN"])


def extract_telegram_token(text):
    return text.split()[1] if len(text.split()) > 1 else None


def get_current_user(chat_id):
    return db.session.query(User).filter_by(telegram_id=chat_id).first()


def send_notification(chat_id, text):
    bot.send_message(chat_id, str(text))


def send_view(chat_id, short_link, ip_address, views_count):
    bot.send_message(
        chat_id, f"New visit for your link ({short_link}) from ip {ip_address}. Total views: {views_count}")


@bot.message_handler(commands=['start'])
def start(message):
    db_user = get_current_user(message.chat.id)
    if db_user:
        bot.send_message(
            message.chat.id, "Hello, {}. You are already authed!".format(db_user.login))
        return
    telegram_token = extract_telegram_token(message.text)
    if telegram_token:
        db_user = db.session.query(User).filter_by(
            telegram_token=telegram_token).first()
        if db_user:
            db_user.telegram_id = message.chat.id
            db.session.add(db_user)
            db.session.commit()
            bot.send_message(
                message.chat.id, "Hello, {}. You are now authed!".format(db_user.login))
        else:
            bot.send_message(
                message.chat.id, f"Auth token not found ({telegram_token})")
        return
    markup = types.ReplyKeyboardMarkup()
    btn_auth = types.InlineKeyboardButton(text="Auth", url=f"{app.config['SERVER_URI']}/tgauth")
    markup.add(btn_auth)

    bot.send_message(message.chat.id, f"Hi. This is a notification bot for Rozlink.\n\n To start please click on this button:", reply_markup=markup)
    


@bot.message_handler(commands=['whoami'])
def whoami(message):
    db_user = get_current_user(message.chat.id)
    if db_user:
        bot.send_message(
            message.chat.id, f"You are {db_user.login}")
    else:
        bot.send_message(message.chat.id, "You are not authed")


@bot.message_handler(commands=['logout'])
def logout(message):
    db_user = get_current_user(message.chat.id)
    if db_user:
        db_user.telegram_id = None
        db.session.add(db_user)
        db.session.commit()
        bot.send_message(message.chat.id, "You are now logged out")
    else:
        bot.send_message(message.chat.id, "You are not authed")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Commands: /start, /whoami, /logout, /help")