import pandas as pd
import ast
import os

# Replace 'your_csv_file.csv' with the actual path to your CSV file.
csv_file_path = 'okr-list.csv'

# Read the CSV file
data = pd.read_csv(csv_file_path)

# Modify the 'owner' column values
for i, row in data.iterrows():
    #data.at[i, 'owner'] = str(i + 1)
    
    # Safely convert the string to a Python dictionary
    data_conv = ast.literal_eval(data.at[i, 'owner'])
    
    # Extract the value of the 'key' key from the 'jiraInfo' dictionary
    key_value = data_conv['jiraInfo']['key']
    
    data.at[i, 'owner'] = key_value


# Write the modified data back to the CSV file
data.to_csv(csv_file_path, index=False)
#print(data)

# Reading the CSV files
df1 = pd.read_csv('okr-list.csv')
df2 = pd.read_csv('okr-user.csv')

# Creating a dictionary from the second CSV
owner_dict = dict(zip(df2['accountId'], df2['id']))

# Function to map owner IDs
def map_owner(row):
    if row['owner'] in owner_dict:
        #owner_id = owner_dict[row['owner']]
        owner_id = {"owner": {"id": owner_dict[row['owner']]}}
        return owner_id
    else:
        return row['owner']

# Applying the function to the first CSV
df1['owner'] = df1.apply(map_owner, axis=1)

# Writing the result back to a CSV file
df1.to_csv('okr-list.csv', index=False)