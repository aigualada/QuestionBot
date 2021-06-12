import logging
import datetime
import pytz
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

QuestionsFile = "WeekQuestions.txt"

def get_day_question(day=0):
    """Returns the question for specific week day (0:monday, 1:tuesday...)."""

    question_file = open(QuestionsFile)
    for position, question in enumerate(question_file):
        if position in [day]:
            return question


def send_daily_question(context: CallbackContext) -> None:
    """Sends daily question to chat"""

    job = context.job

    NumWeekDay = datetime.datetime.today().weekday()

    DayQuestion = get_day_question(NumWeekDay)

    context.bot.send_message(job.context, text=DayQuestion)



def start_scheduler(update: Update, context: CallbackContext) -> None:

    chat_id = update.message.chat_id
    update.message.reply_text("Setting daily question scheduler!.")
    job_removed = remove_job_if_exists(str(chat_id), context)

    try:
        Hour = int(context.args[0])
        Minutes = int(context.args[1])
        TimeZone = context.args[2]

        context.job_queue.run_daily(send_daily_question, datetime.time(hour=Hour, minute=Minutes, tzinfo=pytz.timezone(TimeZone)),
                                days=(0, 1, 2, 3, 4, 5, 6), context=chat_id, name=str(chat_id))

        update.message.reply_text('Question scheduler succesfully set. Bot sends daily question at %d:%d' % (Hour, Minutes)) 

    except(IndexError, ValueError):
        update.message.reply_text("Usage: /set_scheduler <hour> <minutes> <timezone>")
        update.message.reply_text("Example: /set_scheduler 10 0 Europe/Madrid")


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""

    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True  



def main() -> None:

    updater = Updater("BOT_TOKEN")
    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("set_scheduler", start_scheduler))
    
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()