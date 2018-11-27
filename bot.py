import os
import smtplib
import glob
import telepot
import telegram
import tarfile
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

docs = []

def clean():
	files = glob.glob('*.tar')
	for x in files:
		os.remove(x)

def genFiles(mex, docs):
	global infos
	global send

	infos = mex.split('/')
	command = 'echo ' + str(infos[0]) + '> README'
	os.system(command)
	command = 'echo ' + str(infos[1]) + '> INSTALL'
	os.system(command)
	surname = str(infos[3])
	#print(surname)
	now = datetime.now()
	tarName = 'es_' + str(now.year) + str(now.month) + str(now.day) + '_' + surname + '.tar'
	command = 'tar -cf es_' + tarName + ' -T /dev/null'
	#print(command)
	os.system(command)
	archive = tarfile.open(tarName, mode="a")
	archive.add("README", arcname="README")
	archive.add("INSTALL", arcname="INSTALL")
	archive.add("COPYNG", arcname="COPYNG")
	for x in docs:
		archive.add(x, arcname=x)
	archive.close()

def sendMail(user, server):
	global now

	emailTo = str(infos[2])
	email = MIMEMultipart('alternative')
	part = MIMEBase('application', 'octet-stream')
	surname = str(infos[3])
	now = datetime.now()
	send = 'es_' + str(now.year) + str(now.month) + str(now.day) + '_' + surname + '.tar'
	#print(send)
	part.set_payload(open(send, 'rb').read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachement; filename=' + str(send))
	email.attach(part)
	email['Subject'] = '@' + user + 'Pikkio Exercise'
	email['From'] = 'pikkiobot@gmail.com'
	email['To'] = emailTo
	server.sendmail('pikkiobot@gmail.com', emailTo, email.as_string())
	#print("Email Inviata! DONE")

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	clean()

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("pikkiobot@gmail.com", "Pikkiobot01")

	global fileName

	addFile = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="Yes", callback_data="yes"),InlineKeyboardButton(text="No", callback_data="No")]])

	if content_type == 'document':
		print('Download del file in corso ...')
		idFile = msg['document']['file_id']
		fileName = msg['document']['file_name']
		if fileName[len(fileName)-4:] != '.cpp' and fileName[len(fileName)-2:] != '.h' and fileName != 'COPYNG':
			bot.sendMessage(chat_id, "❌ <i>Tipo di file non valido,</i>\n Sono ammessi solamente\n file con estensione \n<b>.cpp</b> o <b>.h</b>", parse_mode='HTML')
		else:
			bot.download_file(idFile, fileName)
			bot.sendMessage(chat_id, "<b>✅ File aggiunto con successo all'archivio!</b>\n\n<i>❓ Altri file? </i>", parse_mode='HTML')
			print('File downloadato con successo!')
			docs.append(fileName)
			#print(docs)
	if content_type == 'text':
		mex = msg['text']
		if mex == '/help':
			bot.sendMessage(chat_id, "FUNZIONAMENTO : \n\n<b>README/INSTALL/EMAIL/COGNOME</b>\n\nEmail --> a cui inviare\nI tre parametri separati da <b>/</b>\n\nCognome --> congome da inserire nel nome del file", parse_mode='HTML')
		elif mex[0] != '/': 	
			user = str(msg['from']['first_name'])
			genFiles(mex, docs)
			send_mes = bot.sendMessage(chat_id, "<i>Invio email a " + str(infos[2]) + " in corso ...</i>", parse_mode='HTML')
			sendMail(user, server)
			send_mes = bot.editMessageText(telepot.message_identifier(send_mes), "<i>Email consegnata con successo!</i>", parse_mode='HTML')

TOKEN = '768658931:AAEuieS0SDJfnjEX0kPDd0meHJlBryWRUT4'
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message})

print('Listening for requests ...')

import time
while 1:
    time.sleep(10)
