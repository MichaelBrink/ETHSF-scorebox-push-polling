from update_helpers import *
from threading import Thread

'''
Using threads for async function execution
'''
if __name__ == '__main__':
    Thread(target = run_score_update).start()
    Thread(target = run_leaderboard, args=("0x691C7c07A1B1698c56340d386d8cC7A823f6e2D8",)).start()


#0x9017804aE02877C32739A7703400326e9Ac9a04d

