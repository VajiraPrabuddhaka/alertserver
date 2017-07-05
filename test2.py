import json
import threading
from threading import Lock
import time
from queue import Queue


#this data models as main data stream
import math

jsonData = open('data.JSON') #sample data
jsonStr_data = jsonData.read()
jsonStr_alerts = open("alerts.JSON").read()
jsonStr_alerts_states = open("alertStates.JSON").read()
alertQueue = Queue()
#manage locks
data_cache_lock = threading.Lock()
alert_list_lock = threading.Lock()
alert_queue_lock = threading.Lock()


def find(Df, ch):
    global jsonStr_data
    json1_data = json.loads(jsonStr_data)
    return (json1_data[str(Df)])[str(ch)]

def compute(exp):
    try:
        return eval(exp,{"__builtins__":None},{"find":find, "math":math})
    except:
        print("Error while parsing the constraint expression")

def checkConstraint(exp):
    global data_cache_lock
    lock = Lock()
    data_cache_lock.acquire()
    try:
        if (compute(exp)):
            return True
        else:
            return False

    finally:
        data_cache_lock.release()


def checkAlerts(time_interval):
    global alert_list_lock, alertList, alertQueue
    while 1:
        time.sleep(time_interval)
        for x in alertList:
            if checkConstraint(x.getConstraint()) and x.getState() :
                try:
                    alert_list_lock.acquire()
                    if not(alertQueue.hasElement(x)) :
                        alertQueue.enqueue(x)
                        #print(x.getTopic())
                finally:
                    alert_list_lock.release()

def addAlert(alert):
    lock = Lock()
    try:
        lock.acquire()
        alertList.append(alert)
    finally:
        lock.release()

def deployAlerts():
    global alertQueue
    while 1:
        time.sleep(1)
        try:
            alertQueue.dequeue()
        except IndexError:
            print ("Error while deploying alerts")

def checkActiveAlerts(time_interval):
    global jsonStr_alerts_states, jsonStr_alerts, alert_queue_lock
    while 1:
        time.sleep(time_interval)
        for x in json.loads(jsonStr_alerts_states):
            if (json.loads(jsonStr_alerts_states)[x]):
                if (checkConstraint(json.loads(jsonStr_alerts)[x]["constraint"])):
                    alert_queue_lock.acquire()
                    try:
                        alertQueue.put(x)

                    finally:
                        alert_queue_lock.release()


jsonStr_alerts = open("alerts.JSON").read()



#demo


threading._start_new_thread(checkActiveAlerts, (1,))
while 1:
    time.sleep(1)
    print (alertQueue.qsize())



















"""
#demo
obj1 = alert("Alert_1", "find('D1', 'ch2') / find('D2', 'ch2') > 0.001", True)
obj2 = alert("Alert_2", "find('D1', 'ch2') + find('D2', 'ch2') > 95", True)
obj3 = alert("Alert_3", "find('D1', 'ch2') + find('D3', 'ch2') < 9935", True)

alertList.append(obj1)
alertList.append(obj2)
alertList.append(obj3)


threading._start_new_thread(checkAlerts, (1,))
threading._start_new_thread(deployAlerts, ())

while 1:
    #checkAlerts(alertList, q1)
    #print (compute("find('D1', 'ch2') + find('D3', 'ch2')"))
    print (alertQueue.size())
    #time.sleep(0.01)
"""