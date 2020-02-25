import logging

from telegram.ext import Updater, CommandHandler
import lsf_logging
import secrets

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
lastHash = ''
timeout = 2
access = False

def start(update, context):
    global access
    global lastHash
    if access:
        lastHash = getNotenspiegelHash()
        context.job_queue.run_repeating(alarm, 2, context=update.message.chat_id)
    else:
        answer(update,"You have no Access. Please /pwd <Password> first!")

def getNotenspiegelHash():
    bot = lsf_logging.LsfBot(secrets.username, secrets.password)
    bot.login()
    bot.selectNotenSeite()
    bot.getNotenSpiegel()
    bot.close()
    return hash(bot.notenSpiegel)

def pwd(update, context):
    global lastHash
    global timeout
    global access
    try:
        if (context.args[0] == secrets.telPassword) or access:
            access = True
            answer(update,"Password Correct! Logged in")
        else:
            answer(update,"Password wrong! Try again!")
    except(IndexError, ValueError):
        answer(update,"Usage: /pwd <Passwort>")

### Returns true if there are new grades
def checkForNewGrades():
    global lastHash
    noten_spiegel_hash = getNotenspiegelHash()
    if noten_spiegel_hash != lastHash:
        lastHash = noten_spiegel_hash
        return True
    else:
        return False

def alarm(context):
    if checkForNewGrades():
        job = context.job
        context.bot.send_message(job.context, text='Es sind neue Noten verfuegbar!!!')

def timeout(update, context):
    global timeout
    global access
    try:
        if not access:
            raise PermissionError
        else:
            timeout = int(context.args[0])
            answer(update, "Set Timeout to {}".format(timeout))
            return
    except(IndexError, ValueError):
        answer(update,"Usage: /timeout <timeout in seconds>")
    except(PermissionError):
        answer(update,"You have no Access. Please /pwd <Password> first!")


def answer(update, text):
    update.message.reply_text(text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(secrets.telToken, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("timeout", timeout))
    dp.add_handler(CommandHandler("pwd", pwd))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
