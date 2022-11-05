from datetime import date
from datetime import datetime
import os
import requests
import time
import requests
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# --- SCORE UPDATE HELPER FUNCTIONS

def get_rows_as_dicts(cursor, table):
    cursor.execute('select * from {}'.format(table))
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def days_between(last_stored_score):
    '''
    Returns differnece in days between 2 days
    '''
    d2 = date.today()#
    d1 =  date.fromtimestamp(last_stored_score)
    d1 = datetime.strptime(str(d1), "%Y-%m-%d")
    d2 = datetime.strptime(str(d2), "%Y-%m-%d")
    return abs((d2 - d1).days)

def get_update():
    conn_string = str('host='+os.environ['host']+' dbname='+os.environ['dbname']+' user='+os.environ['user']+' password='+os.environ['password'])

    with psycopg2.connect(conn_string) as conn, conn.cursor() as cursor:
        dump = [
            get_rows_as_dicts(cursor, 'public.encrypt')
        ]
        
        store_data = dump
        return(store_data[0])

def create_time_list():
    records = get_update()
    newlist= []
    for item in records:
        if not any(item['wallet'] in d['wallet'] for d in newlist):
            newlist.append(item)

    delta_list=[days_between(items['timestamp']) for items in newlist]
    return(delta_list, newlist)

def msg_group(mailing_list):
    
    ls_24=[]
    ls_48=[]
    ls_72=[]

    for item in mailing_list:
        if item[1] == "notify_24":
            ls_24.append(item)
        elif item[1] == "notify_48":
            ls_48.append(item)
        else:
            ls_72.append(item)

    return([{"24":ls_24}, {"48":ls_48}, {"72":ls_72}])
    
def send_score_update():
    '''
    Check which users are eligible for a score update
    '''
    time_list = create_time_list()[0]
    newlist = create_time_list()[1]

    mailing_list= []
    counter=0;

    for n in time_list:

        if (n<1):
            mailing_list.append([newlist[counter]['wallet'], "notify_24"])
            #print ("LESS 1: "+ newlist[counter]['wallet'] + str(n))
        elif ((n > 1) & (n <= 5)):
            mailing_list.append([newlist[counter]['wallet'], "notify_48"])
            #print ("1 - 5: "+ newlist[counter]['wallet'] + str(n))
        elif ((n > 5) & (n <= 10)):
            mailing_list.append([newlist[counter]['wallet'], "notify_72"])
            #print ("5 - 10: "+ newlist[counter]['wallet'] + str(n))
        else:
            #pass
            mailing_list.append([newlist[counter]['wallet'], "notify_72"])
            #print ("NONE FOR: "+ newlist[counter]['wallet'] + str(n))

    return (mailing_list)

msg={"notify_24": str(datetime.today()),
    "notify_48": str(datetime.today()),
    "notify_72": str(datetime.today())}
    

for item in msg_group(send_score_update()): 
    try:
        print (item)
    except:
        pass
 
    # url = os.environ['push_url']

    # querystring = {"recipients":"['eip155:5:0xe9c079525aCe13822A7845774F163f27eb5f21Da','eip155:5:0x691C7c07A1B1698c56340d386d8cC7A823f6e2D8']"}

    # payload = ""
    # headers = {
    #     "title": "tile",
    #     "msg": "Something",
    #     "img": "https://cdn-icons-png.flaticon.com/512/4525/4525688.png"
    # }
    # #response = requests.request("POST", url, data=payload, headers=headers)
\

