from pyrogram import Client
from decouple import config # pip install python-decouple

from pyrogram.types import ReplyKeyboardMarkup as Markup

from re import match

app = Client(
    name="db",
    api_id=config('api_id'),
    api_hash=config('api_hash'),
    bot_token=config('token')
)

{
    123456: {'step': "home", 'name': '', "email": ""},
    789456: {'step': "home", 'name': '', "email": ""},
    654321: {'step': "home", 'name': '', "email": ""}
}

{
    1904997544: {'step': 'home', 'name': 'alireza', 'email': 'alireza@gmail.com'},
    317817082: {'step': 'home', 'name': 'Hamidreza', 'email': 'hamid@gmail.com'}
}

STEP = {}

@app.on_message()
def messages(app, message):
    global STEP

    print(f'New Message from {message.chat.first_name}')  
    
    chat_id = message.chat.id

    if chat_id not in STEP:
        STEP[chat_id] = {'step': "home", 'name': '', "email": ""}

    text = message.text

    # text - step - callback

    commands = [
        [r"/start", r".+", start], # text - step - callback
        [r"cancel", r".+", start],

        [r"signup", r"home", signup],
        [r"Info", r"home", info],

        [r".+", r"enter-full-name", enter_full_name],
        [r".+", r"enter-email-address", enter_email_address],
    ]

    for command in commands:
        pattern, step, callback = command

        if match(pattern, text) and match(step, STEP[chat_id]["step"]):
            callback(message)
            break
    else:
        message.reply_text(text='bad request.')

    # if text in ['/start', 'cancel']:
    #     start(message)
    # elif text == 'signup' and STEP[chat_id]["step"] == 'home':
    #     signup(message)
    # elif text == "Info" and STEP[chat_id]["step"] == 'home':
    #     info(message)
    # elif STEP[chat_id]["step"] == 'enter-full-name':
    #     enter_full_name(message)        
    # elif STEP[chat_id]["step"] == 'enter-email-address':
    #     enter_email_address(message)
    # else:
    #     message.reply_text(text='bad request.')

def start(message):
    chat_id = message.chat.id
    STEP[chat_id]["step"] = 'home'
    message.reply_text(
        text="wellcome to pysoft tutorial.",
        reply_markup=Markup(
            keyboard=[
                ["signup"],
                ["Info"]
                ],
            resize_keyboard=True
        )
    )

def signup(message):
    chat_id = message.chat.id
    STEP[chat_id]["step"] = 'enter-full-name'
    message.reply_text(
        text="enter your full-name: ",
        reply_markup=Markup(
            keyboard=[["cancel"]],
            resize_keyboard=True
        )
    )

def enter_full_name(message):
    chat_id, text = message.chat.id, message.text

    if text.isdigit():
        return message.reply_text(text='please enter your full-name correctly:')

    STEP[chat_id]["step"] = 'enter-email-address'
    STEP[chat_id]['name'] = text
    message.reply_text(
        text="all right, enter your email-address: ",
        reply_markup=Markup(
            keyboard=[["cancel"]],
            resize_keyboard=True
        )
    )

def enter_email_address(message):
    chat_id, text = message.chat.id, message.text
    
    STEP[chat_id]["step"] = 'home'
    STEP[chat_id]['email'] = text

    message.reply_text(
        text="Ok, your informations are saved successfully.\n\nYou have returned to the home page.",
        reply_markup=Markup(
            keyboard=[["signup"], ["Info"]],
            resize_keyboard=True
        )
    )

def info(message):
    chat_id = message.chat.id
    if STEP[chat_id]["name"] and STEP[chat_id]["email"]:
        print(STEP)
        message.reply_text(text=f"Your name is **{STEP[chat_id]['name']}** and your email address is **{STEP[chat_id]['email']}**")
    else:
        message.reply_text(text=f"Your registration is incomplete, please register first.")


app.run()