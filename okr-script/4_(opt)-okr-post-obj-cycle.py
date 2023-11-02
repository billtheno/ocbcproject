import csv
from datetime import datetime
import json
import requests

url = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/objective-cycles'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW5pc3RyYXRvcjppemVubzEyMyEh',
    'Cookie': 'JSESSIONID=DE77C4B238AC211B9BA1AB59A45F3C90; atlassian.xsrf.token=BJQ1-I8SR-CDNY-OY8W_7a52faa8cf9519e350b68d64cf6f7616dc227626_lin'
}

with open('okr-objective-test.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = {
            "title": row['title'],
            "startDate": datetime.strptime(row['displayStartDate'], '%d-%b-%y').strftime('%Y-%m-%d'),
            "dueDate": datetime.strptime(row['displayDueDate'], '%d-%b-%y').strftime('%Y-%m-%d'),
            "message": row['message'],
            "gradingType": int(row['gradingType']),
            "gradingSetting": json.dumps(eval(row['gradingSetting']))
        }
        #print(data)

        response = requests.post(url, json=data, headers=headers)
        print(response.text)
