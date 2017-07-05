import threading

from threading import Lock
from alert import alert
import time
from sympy import *
import json

#json data

#this data models as main data stream
global alertList
alertList = []
global jsonStr_alerts
jsonData = open('data.JSON')
jsonStr_alerts = jsonData.read()





json1_data = json.loads(jsonStr_alerts)

#user defined constraint
#expr = "D1.ch2 + D2.ch2 > 6"
##expr = expr.replace("."," ")

    #jsonTopython = json.loads(jsonData)

    #print (jsonTopython)

    #x = symbols()
    #print (json1_data["D1"]['ch2'])

    #print (json1_data)
    #def _init_(self):


def find(Df, ch):
    global jsonStr_alerts
    json1_data = json.loads(jsonStr)
    return (json1_data[str(Df)])[str(ch)]


def evalx(exp, data): #expression must be given in string format with the correct standard defines here
    json1_data = json.loads(data)
    p_str = exp.replace("."," ")
    s_list = symbols(p_str)
    return (json1_data[str(s_list[0])])[str(s_list[1])]


def compute(exp):
    return eval(exp)


def checkConstraint(exp):
    global jsonStr_alerts
    lock = Lock()
    lock.acquire()
    try:
        if (compute(exp)):
            return true
        else:
            return false

    finally:
        lock.release()  #release lock, no matter what


#print (compute("find('D1', 'ch2') > find('D2', 'ch2')"))

def printCon(exp):
    print (checkConstraint(exp))




def checkAlert(alert):
    while (alert.getState()):
        try:
            if (checkConstraint(alert.getConstraint())):
                print(alert.getTopic(), " is Alerting...")

            else:
                print(alert.getTopic(), " is not alerting...." )
        except ValueError:
            print("Oops!! invalid constraint type")

def checkAlert1(alert):
    try:
        if (checkConstraint(alert.getConstraint())):
            return True

        else:
            return False
    except ValueError:
        print("Oops!! invalid constraint type")
#def alertSet(): #should add newly defined alerts to the array

def changeConstraint(alert, exp):
    alert.updateConstraint(exp)


def addAlert(alert):
    global alertList
    alertList.append(alert)
    threading._start_new_thread(checkAlert, (alert,))


def addAlert2(alert):
    global alertList
    alertList.append(alert)

def checkingAlerts(Alist):
    for x in Alist:
        if (checkAlert1(x)): #generate alert on corresponding topic
            print (x.getTopic())

#demo
obj1 = alert("Alert_1", "find('D1', 'ch2') + find('D2', 'ch2') > 9935", True)
obj2 = alert("Alert_2", "find('D1', 'ch2') + find('D2', 'ch2') > 95", True)
obj3 = alert("Alert_3", "find('D1', 'ch2') + find('D3', 'ch2') < 9935", True)


addAlert(obj1)
addAlert(obj2)
addAlert(obj3)
checker = True


while 1:
    if (checker):
        changeConstraint(obj1, "find('D1', 'ch2') + find('D2', 'ch2') > 9")
        checker = False
    else:
        changeConstraint(obj1, "find('D1', 'ch2') + find('D2', 'ch2') > 3545")
        checker = True


"""
my_objects = []

obj1 = alert("dvej","find('D1', 'ch2') + find('D2', 'ch2') > 35", "Active")
obj2 = alert("qfeew","find('D1', 'ch2') - find('D2', 'ch2') == 35", "Active")


while 1:
    if (checker):
        changeConstraint(obj1, "find('D1', 'ch2') + find('D2', 'ch2') > 9")
        checker = False
    else:
        changeConstraint(obj1, "find('D1', 'ch2') + find('D2', 'ch2') > 9387")
        checker = True

my_objects.append(obj1)
my_objects.append(obj2)

#print (checkConstraint("find('D1', 'ch2') + find('D2', 'ch2') > 35"))

"""