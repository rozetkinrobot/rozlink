from rozlink import app, db
from flask import request, redirect, abort
from flask_login import login_required, logout_user, current_user
from rozlink.utils.bot import create_unique_token
import telebot
from rozlink.telegram_bot import bot

@app.route('/tgauth')
@login_required
def tgauth():
    current_user.telegram_token = create_unique_token()
    db.session.add(current_user)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    print(f"{current_user.login}: {current_user.telegram_token}")
    return redirect("https://telegram.me/{}?start={}".format(app.config["TELEGRAM_BOT_NAME"], current_user.telegram_token))

@app.route(app.config["WEBHOOK_URL_PATH"], methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
