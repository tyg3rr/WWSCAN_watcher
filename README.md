# WWSCAN_watcher README

This project automates the process of fetching, processing, and monitoring Measles detections from the WWSCAN (Wastewater Surveillance) API for Michigan. It identifies new detections and sends email alerts when new cases are found.

# script.py

## Features

- **Fetches latest data** from the WWSCAN API.
- **Filters** for Michigan-specific and Measles-positive samples.
- **Compares** new data with the most recent local data to identify new detections.
- **Saves** new detections and updates local data files.
- **Sends email alerts** via a PowerShell script if new detections are found.
- **Manages local storage** by keeping only the three most recent data files.

## Tools Needed

- Python 3.x
- Windows PowerShell
- Windows Task Scheduler

## File Outputs

- `latest_WWSCAN_data.csv`: Most recent Michigan-specific data from the WWSCAN API.
- `detections/YYYYMMDD.csv`: New detections identified in the latest data, added to a folder containing all detections.
- `data/WWSCAN_YYYYMMDD.csv`: Updated local data file with the latest Measles-specific Michigan data. Note: the date in the filename refers to the most recent *sampling* date. 

## Python Libraries

- pandas
- requests

## Usage

1. Place the script in your working directory.
2. Ensure the `data` and `detections` folders exist.
3. Update the `username` variable in the script to match your Windows username.
4. Ensure `email_alert.ps1` (PowerShell script for email alerts) is present in the same directory.

## Notes

- The python script keeps only the three most recent local data files to save space.
- Email alerts are sent only if new detections are found.
- Make sure you have the necessary permissions to run PowerShell scripts.

---

# email_alert.ps1

This PowerShell script (`email_alert.ps1`) is designed to send automated email alerts when new Measles (MeV) detections are found in Michigan.

## Features

- Sends an email alert to multiple recipients, including email-to-SMS gateways for text notifications.
- Attaches a CSV file containing detection details, with the filename based on the current date.
- Customizable sender, recipients, subject, and body.
- Uses the `Send-MailMessage` cmdlet and a specified SMTP server.

## Requirements 

1. **Configure the script as needed:**
  - Update the `$from`, `$to`, `$smtpServer`, and file paths if necessary.

3. **Attachment:**
  - The script expects a CSV file named with today's date (e.g., `20240613.csv`) in the `WWSCAN_watcher\new_detects\` directory.

## Parameters

- **$date**: Current date in `yyyyMMdd` format, used for the attachment filename.
- **$attachmentPath**: Path to the CSV file to attach.
- **$from**: Sender's email address.
- **$to**: Array of recipient email addresses.
- **$subject**: Email subject line.
- **$body**: Email body content.
- **$smtpServer**: SMTP server for sending the email (contact your health department IT for the server for your health department)

## Notes

- This script is intended for use in a testing environment. The alert system may not be fully accurate.
- Ensure the SMTP server allows relaying from your machine.
- The script requires PowerShell and appropriate permissions to send emails.

## Disclaimer

This automated alert system is still being tested. Please verify all data manually.

---

# Task Scheduler

This tutorial will outline the steps needed to schedule WWSCAN_watcher to run every hour. Windows Task Scheduler is a built-in tool that allows users to automate tasks on their Windows machine. To create the WWSCAN_watcher task, take the following steps:

- Open Task Scheduler

![Task Scheduler main window](images/1.png)

- Create task on the upper right.

- Name the task 

- Add a description (optional)

![image.png](images/2.png)

- Add trigger to begin the task on a schedule; input your desired schedule

![image-2.png](images/3.png)

- Add action

![image-3.png](images/4.png)

  - "Program/script": paste your computer's path to python. For me, that's `C:\Users\jensenl5\AppData\Local\Programs\Python\Python312\pythonw.exe`. Note that it's important to include the 'w' in "pythonw.exe".

  - "Start in (optional)": paste the path to your script directory. For me, that's `C:\Users\jensenl5\Documents\WWSCAN_watcher\`

  - "Add arguments (optional)": paste the name of your script `script.py`

- You're done! You can run the task manually by clicking "run" and you can check when's the last time the code ran by clicking "Refresh"

![image-4.png](images/5.png)

---
## Author

Prepared by: Lillian Jensen

Date started: 06/13/2025
