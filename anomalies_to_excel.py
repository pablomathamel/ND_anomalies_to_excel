import requests
import json
import pandas as pd

#Modify these values to match your environment
nd_cluster="nd_cluster"
nd_auth_domain="nd_auth_domain"
nd_user="nd_user"
nd_pwd="nd_pwd"
##

def get_token():  
   url = nd_cluster+"/login"
   payload = {
        "domain": nd_auth_domain,
        "userName": nd_user,
        "userPasswd": nd_pwd
   }
   headers = {
      "Content-Type" : "application/json"
   }
   requests.packages.urllib3.disable_warnings()
   response = requests.post(url,data=json.dumps(payload), headers=headers, verify=False).json()

   token = response['token']
   return token
def get_anomalies(auth_token): 
   #Uncomment the line below to get the list of anomalies without filters (only active anomalies will be listed)
   url = nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details"
   #Uncomment the line below to get the list of anomalies from a specific date (both active and cleared anomalies will be listed)
   #url = nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details?startDate=2023-10-28"
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

# Specify the name of the Excel file
excel_file = './anomalies_list.xlsx'

# Export the data to an Excel file
df.to_excel(excel_file, index=False)
print(f'Data exported to {excel_file}') 
