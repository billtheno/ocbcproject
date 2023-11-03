import csv
import json
import urllib.request
from urllib import request, parse

url_user = 'http://34.101.196.105:8080/secure/upraise/admin/URUserAction!findUsers.jspa'
url_team = 'http://34.101.196.105:8080/rest/upraiserestservice/1.0/teams'
url_obj = 'http://34.101.196.105:8080/rest/amoeboids-upraise/1.0/okr/objective-cycle'
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

params = {
    'usernames': '',
    'managers': '',
    'designations': '',
    'teams': '',
    'statusIds': '0',
    'role': '',
    'pageSize': '20'
}

# Function to handle HTTP request
def make_request(url, method, headers, data=None):
    req = request.Request(url, data=json.dumps(data).encode('utf-8') if data else None, headers=headers, method=method)
    try:
        with request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode('utf-8'))
    except request.HTTPError as e:
        return e.code, None

# Handling the first request
page = 1
with open('okr-user.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["User ID", "Username", "Full Name", "Role"])  # Write headers

    while True:
        params['page'] = str(page)
        url_with_params = f"{url_user}?{parse.urlencode(params)}"
        req = request.Request(url_with_params, headers=headers)

        try:
            response = request.urlopen(req)
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                if not data['results']:
                    print("No more data available.")
                    break

                for user in data['results']:
                    writer.writerow([user.get('id'), user.get('username'), user.get('fullName'), user.get('role')])

                if not data['hasNext']:
                    print("Data has been successfully written to 'okr-user.csv'.")
                    break

                page += 1
            else:
                print(f"Request failed with status code {response.getcode()}")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

# Handling the second request
response_team = make_request(url_team, 'GET', headers)
if response_team[0] == 200:
    json_data = response_team[1]
    if json_data:
        keys = json_data[0].keys()
        with open('okr-teams.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-teams.csv'.")
    else:
        print("No data found in the response_team.")
else:
    print(f"Request failed with status code {response_team[0]}.")

# Handling the third request
response_obj = make_request(url_obj, 'GET', headers)
if response_obj[0] == 200:
    json_data = response_obj[1]["cycles"]
    if json_data:
        keys = json_data[0].keys()
        with open('okr-objective.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(json_data)
        print("Data has been successfully written to 'okr-objective.csv'.")
    else:
        print("No data found in the response_obj.")
else:
    print(f"Request failed with status code {response_obj[0]}.")

# Handling the fourth request
start_at = 0
results_list = []
while True:
    params = {'startAt': start_at}
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url_okr}?{encoded_params}"
    req = urllib.request.Request(full_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            data_json = json.loads(data)
            results = data_json['results']
            if not results:
                break  # Break the loop if no more results are returned
            results_list.extend(results)
            start_at += 20  # Increment startAt for the next page

    except urllib.error.URLError as e:
        print(f"Error occurred: {e.reason}")
        break

# Save all results to CSV
if results_list:
    with open('okr-list.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(results_list[0].keys())  # Write the header
        for result in results_list:
            writer.writerow(result.values())  # Write the values

    print("Data successfully saved to okr-list.csv")
else:
    print("No results found.")