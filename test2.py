import json
import threading
from threading import Lock
import time
from queue import Queue
from alert import alert

#this data models as main data stream
global alertList
alertList = []
global jsonStr
jsonData = open('data.JSON')
jsonStr = jsonData.read()

def find(Df, ch):
    global jsonStr
    json1_data = json.loads(jsonStr)
    return (json1_data[str(Df)])[str(ch)]

def compute(exp):
    return eval(exp)

def checkConstraint(exp):
    global jsonStr
    lock = Lock()
    lock.acquire()
    try:
        if (compute(exp)):
            return True
        else:
            return False

    finally:
        lock.release()

def checkAlerts(alerts, queue):
    lock = Lock()
    while 1:
        time.sleep(1)
        for x in alerts:
            if checkConstraint(x.getConstraint()):
                try:
                    lock.acquire()
                    if not(queue.hasElement(x)):
                        queue.enqueue(x)
                finally:
                    lock.release()

def addAlert(alert):
    lock = Lock()
    try:
        lock.acquire()
        alertList.append(alert)
    finally:
        lock.release()


#demo

obj1 = alert("Alert_1", "find('D1', 'ch2') / find('D2', 'ch2') > 0.001", "Active")
obj2 = alert("Alert_2", "find('D1', 'ch2') + find('D2', 'ch2') > 95", "Active")
obj3 = alert("Alert_3", "find('D1', 'ch2') + find('D3', 'ch2') < 9935", "Active")

alertList.append(obj1)
alertList.append(obj2)
alertList.append(obj3)

q1 = Queue()
threading._start_new_thread(checkAlerts, (alertList,q1))

while 1:
    #checkAlerts(alertList, q1)
    #print (compute("find('D1', 'ch2') + find('D3', 'ch2')"))
    print (q1.size())
    time.sleep(1)
