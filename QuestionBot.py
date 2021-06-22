import logging
import datetime
import pytz
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Filters
from telegram import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

QuestionsFile = "WeekQuestions.txt"
ReminderTextFile = "ReminderText.txt"

LIST_ADMINS = []


def get_reminder_text():
    reminder_text_file = open(ReminderTextFile)

    return reminder_text_file.read()


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

def send_question_reminder(context: CallbackContext) -> None:
    """Sends daily reminder to the day question"""
    
    job = context.job

    ReminderText = get_reminder_text()

    NumWeekDay = datetime.datetime.today().weekday()
    DayQuestion = get_day_question(NumWeekDay)
    
    context.bot.send_message(job.context, text=ReminderText + "\n" + DayQuestion)



def start_scheduler(update: Update, context: CallbackContext) -> None:
    
    chat_id = update.message.chat_id
    update.message.reply_text("Setting daily question scheduler!.")
    job_removed = remove_job_if_exists(str(chat_id), context)

    try:
        Hour = int(context.args[0])
        Minutes = int(context.args[1])
        HoursReminder = int(context.args[2])
        TimeZone = context.args[3]
        
        context.job_queue.run_daily(send_daily_question, datetime.time(hour=Hour, minute=Minutes, tzinfo=pytz.timezone(TimeZone)), 
                                    days=(0, 1, 2, 3, 4, 5, 6), context=chat_id, name=str(chat_id))

        context.job_queue.run_daily(send_question_reminder, datetime.time(hour=Hour + HoursReminder, minute=Minutes, tzinfo=pytz.timezone(TimeZone)), 
                                    days=(0, 1, 2, 3, 4, 5, 6), context=chat_id, name=str(chat_id))

        update.message.reply_text('Question scheduler succesfully set. Bot sends daily question at %d:%d (%s) and the question reminder at %d:%d (%s) '  
                                    % (Hour, Minutes, TimeZone, Hour + HoursReminder, Minutes, TimeZone)) 

    except(IndexError, ValueError):
        update.message.reply_text("Usage: /set_scheduler <hour> <minutes> <hours_reminder> <timezone> ")
        update.message.reply_text("Example: /set_scheduler 10 30 4 Europe/Madrid\nThe scheduler sends question daily at 10:30 in timezone Europe/Madrid and question reminder 4 hours later at 14:30")


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

    dispatcher.add_handler(CommandHandler("set_scheduler", start_scheduler, Filters.user(username=LIST_ADMINS)))
    
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()