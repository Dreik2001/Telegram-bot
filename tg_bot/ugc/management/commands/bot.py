from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.utils.request import Request
from django.db import migrations, transaction
from django.db import models

from ugc.models import Message
from ugc.models import Profile
from ugc.models import*

def log_errors(f):

	def inner(*args, **kwargs):
		try:
		
			return f(*args, **kwargs)
		except Exception as e:
			error_message = f"Error : {e}"
			
		
			raise e
	return inner
   
 
@log_errors
def do_echo(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id
	text = update.message.text
	name = update.message.from_user
	update_id = update.update_id
	message_id = update.message.message_id
	date = update.message.date
	user_name = update.message.from_user.name


	print(update_id)

	p, created = Profile.objects.get_or_create(
			external_id=chat_id,
			defaults={
				'name': update.message.from_user.username,
			}
		)

	p.save()
	m = Message(
		profile=p,
		text=text,
		)
	m.save()


	reply_text = """  "update_id":   "{}"\n"message":  \n\t"message_id":   "{}",\n\t"from":\t {}\n\t"chat":  \n\t"id":   "{}",\n\t"first_name":   "{}",\n\t"type":   "{}" \n\t\t"date":   "{}",\n\t\t"text":   "{}" \n   \t""".format(update_id, message_id, name, chat_id, user_name, chat_id, date, text)
	update.message.reply_text(
		text=reply_text,
		)


@log_errors
def do_count(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id

	p, created = Profile.objects.get_or_create(
		external_id=chat_id,
		defaults={
			'name': update.message.from_user.username,
		})

	p.save()
	count = Message.objects.filter(profile=p).count()

	update.message.reply_text(
		text=f'You have {count} messages',
		)



class Command(BaseCommand):
	help = 'Telegram-bot'

	def handle(self, *args, **options):
		request = Request(
			connect_timeout=0.5,
			read_timeout=1.0,
			)
		bot = Bot(
			request=request,
			token=settings.TOKEN,
			base_url=settings.PROXY_URL,
			)
		print(bot.get_me())

		updater = Updater(
			bot=bot,
			use_context=True,
			)

		message_handler = MessageHandler(Filters.text, do_echo)
		updater.dispatcher.add_handler(message_handler)

		message_handler2 = CommandHandler('count', do_count)
		updater.dispatcher.add_handler(message_handler2)

		updater.start_polling()
		updater.idle()

