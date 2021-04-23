
#for i in range(1, 1001):
#    if i%3==0 and i%5==0:
#        print(i, "FizzBuzz")
#    elif i%3==0:
#        print(i, "Fizz")
#    elif i%5==0:
#        print(i, "Buzz")
#    else:
#        print(i)
#


#from Tkinter import *
#master = Tk()
#
#w = Canvas(master, width=250, height=200)
#w.create_rectangle(0, 0, 100, 100, fill="blue", outline = 'blue')
#w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
#w.pack()
#master.mainloop()
#

import requests
import json
from pprint import pprint

def createAccount(user):
    url = "https://xpowerwebapi20200430054944.azurewebsites.net/api/User/CreateUserAccount"

    input = {"Username": user,
      "Password": "string",
      "Email": "string",
      "SchoolName": "string",
      "Avatar": True,
      "Avatarimageurl": "string",
      "TouchIdOn": True
    }

    response = requests.post(url, data = input)
    print(response.text)

def getTable():
    
    get1 = requests.get("https://xpowerwebapi20200430054944.azurewebsites.net/api/Point/PointsTable")
    #pprint(get1.text)

    table = json.loads(get1.content)
    return table

def addDeed(user, deed, Date):
    url2 = "https://xpowerwebapi20200430054944.azurewebsites.net/api/Point/Adddeeds"
    
    input = {"Username": user+'1', "Deed": deed, "Date": Date}
    post2 = requests.post(url2, data = input)
    return post2.content

def getTotalPoints(table):
    
    url3 = "https://xpowerwebapi20200430054944.azurewebsites.net/api/Point/GetDailyPoint?Username=bayan"
    sum = 0
    for i in range(len(table)):
       sum+=table[i]['Point']
        
    #post3 = requests.post(url3, data = sum)
    pprint(sum)

createAccount("Ngarg")
table = getTable()
user ="Ngarg"
deed = "descriptions"
data= "2021-03-9"
print(addDeed(user, deed, data))
pprint(table)
print(getTotalPoints(table))
