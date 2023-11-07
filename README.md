## README.md

## Overview

This script queries Cisco Nexus Dashboard Insights application (NDI) for the current anomalies list and exports the data into an excel spreadsheet, following the same format (same columns) as shown in the Anomalies section in the GUI, as follows:

"What's wrong" | "Anomaly Level" | "Category" | "Site" | "Detection Time" | "Title" | "Nodes" | "Status" | "Last Seen Time" | "Cleared"

## REST vs Offline 

Two different scripts are provided. From a JSON payload processing point of view, they work exactly the same. However, the JSON data source is different for each one: REST script interacts directly with NDIs REST API to make the data extraction easier, however that requires NDI to be reachable to where the script is run. Where that is not possible, a manual REST API call can be made using the following URI: 
"https://<nd-cluster>/sedgeapi/v1/cisco-nir/api/api/v1/anomalies/details?filter=cleared%3Afalse+AND+acknowledged%3Afalse&siteGroupName=default&offset=0&count=10000&siteStatus=online"
The resulting response can be manually copied into a json file, and then processed using the Offline script.

## Dependencies

This script has the following dependencies:

- Python3
- Requests
- Json
- Pandas


