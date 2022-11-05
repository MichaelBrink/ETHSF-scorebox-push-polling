from update_helpers import *
import threading

'''
Using threads for async function execution
'''
e = threading.Event()
t1 = threading.Thread(target=run_score_update(15)) #runs every 15 seconds
t1.start()
