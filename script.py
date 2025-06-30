################################################################
################################################################
##          Automating WWSCAN Measles data fetch,             ## 
##                process, and email alerts.                  ##
################################################################
################################################################
##  Purpose: Automating monitoring and email alerts for 
#            WWSCAN Measles detections in Michigan.
##  Input files: WWSCAN API data file (.csv)
##  Prepared by: Lillian Jensen
##  Date started: 06/13/2025
##  Modifications/date: 	
##
################################################################

"""
Workflow:
1. Load the most recent local data file (saved in prior run) and filter for measles detections.
2. Fetch the latest data from WWSCAN's API and filter for Michigan-specific data.
3. Identify new detections by comparing the latest data with the local data.
4. Save new detections to a file and execute the email-alert PowerShell script if new detections exist.
5. Update the local data file with the latest sample date and remove older files.

File Outputs:
- 'latest_WWSCAN_data.csv': Contains most recent Michigan-specific data from the API.
- 'detections/YYYYMMDD.csv': Contains new detections identified in the latest data.
- 'data/WWSCAN_YYYYMMDD.csv': Updated local data file with the latest measles-specific Michigan data.

Notes:
- The script removes older local data files, keeping only the three most recent ones, to preserve memory.
"""

import pandas as pd
import requests
from io import StringIO
from datetime import datetime
import subprocess
import glob
import os

# Define the folder path where local data files are stored
username = "jensenl5"
folder_path = f"C:\\Users\\{username}\\Documents\\measles\\WWSCAN_watcher\\data\\"
files_path = os.path.join(folder_path, '*')

# Retrieve all files in the folder and sort them by creation time
files = sorted(glob.iglob(files_path), key=os.path.getctime)

# Load the most recent local data file and filter for measles detections
if len(files) == 0:
  # If no local data files exist, create an empty DataFrame with the expected columns
  most_recent_measles_data = pd.DataFrame(
    columns=[
      'City',
      'Site_Name',
      'Collection_Date',
      'MeV_gc_g_dry_weight',
      'MeV_gc_g_dry_weight_UCI',
      'MeV_gc_g_dry_weight_LCI'
    ]
  )
else:
  # If local data files exist, load the most recent one
  most_recent_measles_data = pd.read_csv(files[-1])

  # Filter for rows with measles detections (MeV_gc_g_dry_weight > 0)
  most_recent_measles_data = most_recent_measles_data.loc[
    most_recent_measles_data['MeV_gc_g_dry_weight'] > 0
  ]

  # Ensure 'Collection_Date' is in datetime format
  most_recent_measles_data['Collection_Date'] = pd.to_datetime(
    most_recent_measles_data['Collection_Date']
  )

# Fetch the latest data from WWSCAN's API
api = "input WastewaterSCAN API url here." # Reach out to WastewaterSCAN to ask for the url if needed
res = requests.get(api)

if res.status_code == 200:
  # Parse the CSV data from the API response
  csv_data = StringIO(res.text)
  updated_api_data = pd.read_csv(csv_data, low_memory=False)
else:
  print("Failed to fetch data")

# Filter the data for Michigan-specific entries
updated_api_data = updated_api_data.loc[updated_api_data['State'] == 'Michigan'] # Change to your state of interest
updated_api_data = updated_api_data[[
                                    'City',
                                    'Site_Name',
                                    'Collection_Date',
                                    'MeV_gc_g_dry_weight',
                                    'MeV_gc_g_dry_weight_UCI',
                                    'MeV_gc_g_dry_weight_LCI',
                                  ]]

# Remove rows with missing measles detection values
updated_api_data = updated_api_data.loc[updated_api_data['MeV_gc_g_dry_weight'].isna() == False]
updated_api_data['Collection_Date'] = pd.to_datetime(updated_api_data['Collection_Date'])

# Save the filtered Michigan-specific data to a file for human-reference
updated_api_data.to_csv('latest_WWSCAN_data.csv')

# Filter for rows with measles detections
updated_api_data_detections = updated_api_data.loc[updated_api_data['MeV_gc_g_dry_weight'] > 0]

# Compare the latest data with the old data to identify new detections
merged_updated_api_data = updated_api_data_detections\
                            .merge(most_recent_measles_data, how='left', indicator=True)
detections = merged_updated_api_data.loc[merged_updated_api_data['_merge'] == 'left_only']\
                .drop(columns=['_merge'])

# If new detections exist, save them to a file and execute the email-alert script
if len(detections) > 0:
  detections.to_csv(f'detections\\{datetime.today().strftime("%Y%m%d")}.csv')
  subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "email_alert.ps1"], 
                 capture_output=True, text=True)

# Update the local data file with the latest sample date
updated_api_data['Collection_Date'] = pd.to_datetime(updated_api_data['Collection_Date'])
latest_sample_date = updated_api_data['Collection_Date'].max().strftime('%Y%m%d')
updated_api_data.to_csv(f'data\\WWSCAN_{latest_sample_date}.csv')

# Remove older local data files, keeping only the three most recent ones
files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
for f in files[3:]:
  os.remove(f)
