import requests
import json
import variables
from datetime import date, timedelta

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
   
def get_anomalies(): 
   url = variables.nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details?includeAnomalies=all&siteStatus=all"
   json_anom=requests.get(url,headers=headers, verify=False).json()
   with open('anomalies_details.json', 'a') as file:
        json.dump(json_anom, file)
   return json_anom

def get_anomaly_details(anomalies):
    today = date.today()
    weekago = today - timedelta(days = 7) 
    url_impact = variables.nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/siteGroups/default/sites/"+anomalies[1]+"/anomalies/impact?anomalyId="+anomalies[0]+"&startDate="+str(weekago)+"&endDate="+str(today)
    json_impact=requests.get(url_impact,headers=headers, verify=False).json()
    url_rec=variables.nd_cluster+"/sedgeapi/v1/cisco-nir/api/api/v1/siteGroups/default/sites/"+anomalies[1]+"/anomalies/recommendations?anomalyId="+anomalies[0]+"&startDate="+str(weekago)+"&endDate="+str(today)
    json_rec=requests.get(url_rec,headers=headers, verify=False).json()
    with open('anomalies_details.json', 'a') as file:
        json.dump(json_impact, file)
        json.dump(json_rec, file)
        file.close()

# Store anomalies in a python dictionary.

auth_token=get_token()
headers = {
      "Content-Type" : "application/json",
      "Cookie" : "AuthCookie="+auth_token
   }


anomalies_list=get_anomalies()

#Iterate through the anomalies dictionary, and construct a list with the relevant fields of each anomaly
for A in anomalies_list["entries"]:
    anomaly_ids=[]
    anomaly_ids.append((A["anomalyId"],A["siteName"]))

for A in anomaly_ids:
   get_anomaly_details(A)
