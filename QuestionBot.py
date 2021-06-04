import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main() -> None:

    updater = Updater("TOKEN_BOT")
    
    dispatcher = updater.dispatcher

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()