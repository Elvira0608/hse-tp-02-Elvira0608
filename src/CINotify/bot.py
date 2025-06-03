import bot_config
import telebot
from pathlib import Path
import json

bot = telebot.TeleBot(bot_config.token)

@bot.message_handler(content_types=["text"])
def send_notification(status: bool):
    if(status):
        bot.send_message(bot_config.chat_id, bot_config.message_when_passed, "Markdown")
    else:
        bot.send_message(bot_config.chat_id, bot_config.message_when_failed, "Markdown")

def check_test_status():
    if(Path("report.json").is_file()):
        with open("report.json", 'r') as file:
            data = json.load(file)

    if("failed" in data):
        failed_tests = int(data["report"]["summary"]["failed"])
    else:
        failed_tests = 0
        
    if(failed_tests > 0):
        print(data["report"]["summary"]["failed"])
        return False
    else:
        return True

if __name__ == '__main__':
    if(Path("report.json").is_file()):
        if(check_test_status()):
            send_notification(True)
        else:
            send_notification(False)
