import csv
import requests

url = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/directory/teams'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW5pc3RyYXRvcjppemVubzEyMyEh',
    'Cookie': 'JSESSIONID=DE77C4B238AC211B9BA1AB59A45F3C90; atlassian.xsrf.token=BJQ1-I8SR-CDNY-OY8W_7a52faa8cf9519e350b68d64cf6f7616dc227626_lin'
}

with open('okr-teams.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = {
            "name": row['name']
        }

        response = requests.post(url, json=data, headers=headers)
        print(response.text)
