import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

QuestionsFile = "ROUTE_TO_QUESTIONS_FILE"

def get_day_question(day=0):
    #Returns the question for specific week day (0:monday, 1:tuesday...).

    question_file = open(QuestionsFile)
    for position, question in enumerate(question_file):
        if position in [day]:
            return question


def main() -> None:

    updater = Updater("TOKEN_BOT")
    
    dispatcher = updater.dispatcher

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()