from update_helpers import *
import threading

'''
Using threads for async function execution
'''
# e = threading.Event()
# t1 = threading.Thread(target=run_score_update(15)) #runs every 15 seconds
# t1.start()
# print("Score update thread started")

# t2 = threading.Thread(target=run_leaderboard(15, "0x9017804aE02877C32739A7703400326e9Ac9a04d"))
# t2.start()
# print("Leaderboard thread started")

def run(func1, func2):
    while True:
        func1
        func2
        time.sleep(15)

run(run_score_update(),run_leaderboard("0x9017804aE02877C32739A7703400326e9Ac9a04d"))