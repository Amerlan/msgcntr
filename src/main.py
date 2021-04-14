from aiogram import types, Dispatcher, Bot, executor
from dotenv import load_dotenv
import json
import os

load_dotenv()
# APP_NAME = os.getenv('APP_NAME')
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)
# WEBHOOK_HOST = f'https://{APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
# WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# WEBAPP_PORT = int(os.getenv('PORT'))
# WEBAPP_HOST = '0.0.0.0'


with open('counter.json', 'r') as outfile:
    content = outfile.readline()
    msgs = json.loads(content)


@dp.message_handler(commands=['count'])
async def count(msg: types.Message):
    chat_id = str(msg.chat.id)
    text = f"Топ спамеров за всё время:\n"
    cnt = 1
    if chat_id in msgs.keys():
        top_list = sorted(msgs[chat_id].items(), key=lambda item: item[1], reverse=True)
        for name, amount in top_list:
            text += f"{cnt}. @{name} - {amount}\n"
            cnt += 1
    await msg.reply(text=text)


@dp.message_handler()
async def counter(msg: types.Message):
    chat_id = str(msg.chat.id)
    user_identifier = f'{msg.from_user.username}'
    if chat_id in msgs.keys():
        try:
            msgs[chat_id][user_identifier] += 1
        except:
            msgs[chat_id][user_identifier] = 1
    else:
        msgs[chat_id] = {}
        msgs[chat_id][user_identifier] = 1
    with open('counter.json', 'w') as outfile:
        json.dump(msgs, outfile)

#
# async def on_startup(dp):
#     await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, reset_webhook=False, skip_updates=True)
    # start_webhook(
    #     dispatcher=dp,
    #     webhook_path=WEBHOOK_PATH,
    #     skip_updates=True,
    #     on_startup=on_startup,
    #     host=WEBAPP_HOST,
    #     port=WEBAPP_PORT,
    # )
