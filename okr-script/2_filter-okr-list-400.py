import csv

# Replace 'your_csv_file.csv' with the actual path to your CSV file.
csv_file_path = 'okr-list.csv'

# Read the CSV file
with open(csv_file_path, 'r') as file:
    data = list(csv.DictReader(file))

# Modify the 'owner' column values
for row in data:
    owner_str = row['owner']
    owner_dict = eval(owner_str)
    key_value = owner_dict['jiraInfo']['key']
    row['owner'] = key_value

# Write the modified data back to the CSV file
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

# Reading the CSV files
with open('okr-list.csv', 'r') as file1, open('okr-user.csv', 'r') as file2:
    reader1 = csv.DictReader(file1)
    reader2 = csv.DictReader(file2)
    df1 = list(reader1)
    df2 = list(reader2)

# Creating a dictionary from the second CSV
owner_dict = {row['username']: row['id'] for row in df2}

# Function to map owner IDs
def map_owner(row):
    if row['owner'] in owner_dict:
        owner_id = {"owner": {"id": owner_dict[row['owner']]}}
        return owner_id
    else:
        return row['owner']

# Applying the function to the first CSV
for row in df1:
    row.update(map_owner(row))

# Writing the result back to a CSV file
with open('okr-list.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=df1[0].keys())
    writer.writeheader()
    writer.writerows(df1)
