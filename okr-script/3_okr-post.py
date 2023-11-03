import csv
import json
from datetime import datetime
from urllib import request

url = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/objectives'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW5pc3RyYXRvcjppemVubzEyMyEh',
    'Cookie': 'JSESSIONID=DE77C4B238AC211B9BA1AB59A45F3C90; atlassian.xsrf.token=BJQ1-I8SR-CDNY-OY8W_7a52faa8cf9519e350b68d64cf6f7616dc227626_lin'
}

with open('okr-list.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = {
            "type": 1,
            "objectiveCycle": eval(row['objectiveCycle']),
            "owner": {'id': eval(row['owner'])['owner']['id']},
            "labels": eval(row['labels']),
            "title": row['title'],
            "team": eval(row['team']),
            "startDate": datetime.strptime(row['startDate'], '%d-%b-%y').strftime('%Y-%m-%d'),
            "dueDate": datetime.strptime(row['dueDate'], '%d-%b-%y').strftime('%Y-%m-%d'),
            "level": eval(row['level']),
            "visibility": 1,
            "sharedTeams" : [],
            "sharedUsers" : []
        }
        
        req = request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
        try:
            with request.urlopen(req) as response:
                print(response.read().decode('utf-8'))
        except request.HTTPError as e:
            print(f"Request failed with status code {e.code}.")
