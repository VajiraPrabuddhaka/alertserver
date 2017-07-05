import json

jsonData = open('data.JSON') #sample data
jsonStr_alerts = jsonData.read()
json1_data = json.loads(jsonStr_alerts)

for x in json1_data:
    print (x)