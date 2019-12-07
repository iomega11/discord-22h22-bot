import schedule
import threading
import time
import os

import bot
	
class thread22h22(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            schedule.run_pending()
            time.sleep(1)

token = os.environ['TOKEN']

thread = thread22h22()
thread.start()
client = bot.Bot()
client.run(token)