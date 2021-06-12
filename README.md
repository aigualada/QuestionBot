## Simple Question Bot for Telegram

- Sends daily question that reads from txt file.

### Installation

Install requirements with `pip3`:
```
[sudo] pip3 install -r requirements.txt
```

Execute:
```
python3 QuestionBot.py
```

Change BOT_TOKEN by your created bot token. [How to create a bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
The file WeekQuestions.txt its a sample file. Use your own file with the questions you want. Each line of the file corresponds to weekday , first line Monday, second Tuesday ...

### Usage

```
/set_scheduler 12 15 Europe/Madrid 
```
The bot will send the question daily at 12:15 in timezone Europe/Madrid
