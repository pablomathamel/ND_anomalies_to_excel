import requests
import json
import pandas as pd
import openpyxl
import variables

# The values of nd_auth_domain, nd_user, nd_pwd, and nd_cluster, 
# are imported from file "variables.py" which should be created in the same directory 
# where the script is running from. This file is ignored by Git.

def get_token():  
   url = variables.nd_cluster+"/login"
   payload = {
        "domain": variables.nd_auth_domain,
        "userName": variables.nd_user,
        "userPasswd": variables.nd_pwd
   }
   headers = {
      "Content-Type" : "application/json"
   }
   requests.packages.urllib3.disable_warnings()
   response = requests.post(url,data=json.dumps(payload), headers=headers, verify=False).json()
   token = response['token']
   return token
   
def get_anomalies(auth_token): 
   #The line below is a similar API call as made from NDI GUI.
   url = variables.nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details?filter=cleared%3Afalse+AND+acknowledged%3Afalse&siteGroupName=default&offset=0&count=10000&siteStatus=online"
   headers = {
      "Content-Type" : "application/json",
      "Cookie" : "AuthCookie="+auth_token
   }
   return requests.get(url,headers=headers, verify=False).json()

# Store anomalies in a python dictionary.
anomalies_list=get_anomalies(get_token())
all_anomalies=[]

#Iterate through the anomalies dictionary, and construct a list with the relevant fields of each anomaly
for A in anomalies_list["entries"]:
    single_anomaly=[]
    single_anomaly.append(A["anomalyReason"])
    single_anomaly.append(A["severity"])
    single_anomaly.append(A["category"])
    single_anomaly.append(A["fabricName"])
    single_anomaly.append(A["startDate"])
    single_anomaly.append(A["mnemonicTitle"])
    single_anomaly.append(A["nodeNames"])
    if not A["clearDate"]:  
        single_anomaly.append("Active")
    else:
        single_anomaly.append("Cleared")
    single_anomaly.append(A["endDate"])
    single_anomaly.append(A["clearDate"])  
    all_anomalies.append(single_anomaly)

 # Convert the list to a Pandas DataFrame
df = pd.DataFrame(all_anomalies, columns=["What's wrong","Anomaly Level","Category","Site","Detection Time","Title","Nodes","Status","Last Seen Time","Cleared"])

json_file = './anomalies_list.json'
df.to_json(json_file,index=False)

# Specify the name of the Excel file
excel_file = './anomalies_list.xlsx'

# Export the data to an Excel file
df.to_excel(excel_file, index=False)
print(f'Data exported to {excel_file}') 
