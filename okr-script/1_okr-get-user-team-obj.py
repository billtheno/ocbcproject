import requests
import csv

url_user = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/directory/users/get-all'
url_team = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/directory/teams'
url_obj = 'http://34.101.196.105:8080/rest/upraisesuccess/latest/objective-cycles'
url_okr = 'http://34.101.196.105:8080/rest/amoeboids-upraise/1.0/okr/search'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW5pc3RyYXRvcjppemVubzEyMyEh',
    'Cookie': 'JSESSIONID=41F9907CB650F18C62481146A08232FD; atlassian.xsrf.token=BJQ1-I8SR-CDNY-OY8W_59412b0dcbf39061d7cf2e9cdb9ab5e911bd1eba_lin'
}

data = {
    "filters": None,
    "pageNumber": 0,
    "pageSize": 20,
    "sortBy": "displayName",
    "sortDirection": "ASC",
    "setDirectReports": True,
    "viewId": 6
}

response_user = requests.post(url_user, headers=headers, json=data)

# Check if the request was successful
if response_user.status_code == 200:
    # Extract the content from the JSON response_user
    json_data = response_user.json()["content"]
    if json_data:
        # Extract keys to form the CSV header
        keys = json_data[0].keys()
        with open('okr-user.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-user.csv'.")
    else:
        print("No data found in the response_user.")
else:
    print(f"Request failed with status code {response_user.status_code}.")
    

response_team = requests.get(url_team, headers=headers)

# Check if the request was successful
if response_team.status_code == 200:
    # Extract the content from the JSON response_team
    json_data = response_team.json()["content"]
    if json_data:
        # Extract keys to form the CSV header
        keys = json_data[0].keys()
        with open('okr-teams.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-teams.csv'.")
    else:
        print("No data found in the response_team.")
else:
    print(f"Request failed with status code {response_team.status_code}.")
    

response_obj = requests.get(url_obj, headers=headers)

# Check if the request was successful
if response_obj.status_code == 200:
    # Extract the content from the JSON response_obj
    json_data = response_obj.json()["content"]
    if json_data:
        # Extract keys to form the CSV header
        keys = json_data[0].keys()
        with open('okr-objective.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-objective.csv'.")
    else:
        print("No data found in the response_obj.")
else:
    print(f"Request failed with status code {response_obj.status_code}.")


response_okr = requests.get(url_okr, headers=headers)

# Check if the request was successful
if response_okr.status_code == 200:
    # Extract the content from the JSON response_okr
    json_data = response_okr.json()["results"]
    if json_data:
        # Extract all unique keys to form the CSV header
        keys = set()
        for obj in json_data:
            keys.update(obj.keys())
        with open('okr-list.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-list.csv'.")
    else:
        print("No data found in the response_okr.")
else:
    print(f"Request failed with status code {response_okr.status_code}.")
