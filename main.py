from update_helpers import *
import threading
from threading import Thread
import time
import schedule


'''
Using threads for async function execution
'''

schedule.every(1).minutes.do(run_score_update)

while 1:
    schedule.run_pending()
    time.sleep(1)
