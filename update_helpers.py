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
        #print(store_data[0])
        return(store_data[0])

def create_time_list():
    records = get_update()
    newlist= []
    for item in records:
        if not any(item['wallet'] in d['wallet'] for d in newlist):
            newlist.append(item)

    delta_list=[days_between(items['timestamp']) for items in newlist]
    #print(newlist)
    return(delta_list, newlist)


#print(create_time_list()[1][2]['wallet'])

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
            pass
            #mailing_list.append([newlist[counter]['wallet'], "notify_72"])
            #print("ISSUE!")
            #print ("NONE FOR: "+ newlist[counter]['wallet'] + str(n))
        
        counter=counter+1

    return (mailing_list)


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

    return([{"notify_24":ls_24}, {"notify_48":ls_48}, {"notify_72":ls_72}])

#print(msg_group(send_score_update()))

msg={"notify_24": "Score ready for update in 1 day | "+str(datetime.today()),
    "notify_48": "Score ready for update in 2 days | "+str(datetime.today()),
    "notify_72": "Score ready for update in 3 day | "+str(datetime.today())}

def converter(example):
    output = []
    for n in example:
        if "." not in n[0]:
            newstring="eip155:5:"+n[0]
            output.append(newstring)
        else:
            pass
    return(output)

def run_score_update(duration):
    for item in msg_group(send_score_update()):
        url = "http://localhost:8080/api"

        #print(msg[list(item.keys())[0]])
        querystring = {"recipients":str(converter(item[list(item.keys())[0]]))}

        payload = ""
        headers = {
            "title": "Score update ready!",
            "msg": msg[list(item.keys())[0]],
            "img": "https://cdn-icons-png.flaticon.com/512/5334/5334827.png "
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    time.sleep(duration)

#recipients=converter(item[list(item.keys())[0]])
# example=['0x9017804aE02877C32739A7703400326e9Ac9a04d', 'notify_24'], ['0xe9c079525aCe13822A7845774F163f27eb5f21Da', 'notify_24'], ['0x9022a898B401d368cBa4023ef375beEF165a8128', 'notify_24'], ['0x61ec3Cd93E62a858408c92bdec903304c4C5436e', 'notify_24'], ['0xFa37d93a18Ed35139785629840B62f7C3aE7d088', 'notify_24']