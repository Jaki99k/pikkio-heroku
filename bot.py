import telepot
import telegram
import urllib.request
from InstagramAPI import InstagramAPI
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


client = InstagramAPI("jakybay", "camillo197")

client.login()

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    
    global mex
    mex = msg['text']

    if content_type == 'text':
            answerMex = ""
            client.searchUsername(mex)
            userInfo = client.LastJson
            print("Richiesto : ", mex)
            #print(userInfo)
            answerMex = "🔮Details : \n\n"
            if str(userInfo['user']['full_name']) != "":
                answerMex += "<b>🗣️Full Name :  </b>" + str(userInfo['user']['full_name']) + '\n'
            answerMex += "<b>👨‍Username :  </b>" + str(userInfo['user']['username']) + '\n\n\n'
            answerMex += "<b>📸Published Photos :  </b>" + str(userInfo['user']['media_count']) + '\n'
            answerMex += "<b>⏮️Followers :  </b>" + str(userInfo['user']['follower_count']) + '\n'
            answerMex += "<b>⏭️Following :  </b>" + str(userInfo['user']['following_count']) + '\n\n\n'
            if str(userInfo['user']['is_private']) == 'True':
                answerMex += "<b>🔐Private Profile :  </b>" + '✅' + '\n\n\n'
            else:
                answerMex += "<b>🔐Private Profile :  </b>" + '❌' + '\n\n\n'
            answerMex += "<b>📝Biography :  </b>\n\n" + str(userInfo['user']['biography']) + '\n' 
            bot.sendMessage(chat_id, answerMex, parse_mode='HTML')
            form = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🖼 Download Profile Pic ", callback_data="profilepic")]
            ])
            bot.sendMessage(chat_id, "<b>👽EXTRA : </b>", reply_markup=form, parse_mode='HTML')
            #bot.sendPhoto(chat_id, ("profile_pic.jpg", ))

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'profilepic':
            client.searchUsername(mex)
            userInfo = client.LastJson
            print(userInfo)
            url = userInfo['user']['hd_profile_pic_url_info']['url']
            photo = urllib.request.urlopen(url)
            bot.sendPhoto(from_id, ("profile_pic.jpg", photo))


TOKEN = "703552342:AAFbaj2jDZ11ZTT60LMbZHBw34yR0YLFG0w"
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})

import time
while 1:
    time.sleep(10)
