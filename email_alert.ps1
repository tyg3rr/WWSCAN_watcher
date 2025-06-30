<#
.SYNOPSIS
Sends an email alert with an attachment if detections are found.

.DESCRIPTION
This script generates an email alert with a dynamically generated attachment file based on today's date. 
The email contains information about a new Measles detection in Michigan and is sent to multiple recipients. 
The script uses the `Send-MailMessage` cmdlet to send the email.

.PARAMETER $date
The current date in "yyyyMMdd" format, used to dynamically generate the file path for the attachment.

.PARAMETER $attachmentPath
The file path of the attachment, which includes the dynamically generated date.

.PARAMETER $from
The sender's email address.

.PARAMETER $to
An array of recipient email addresses, including email-to-SMS gateways for text alerts.

.PARAMETER $subject
The subject line of the email.

.PARAMETER $body
The body content of the email, providing details about the detection and a disclaimer about the system's testing status.

.PARAMETER $smtpServer
The SMTP server used to send the email.

#>

# Output an alert message to PowerShell

# Generate today's date in yyyyMMdd format
$date = Get-Date -Format "yyyyMMdd"

# Define the file path with the dynamic date
$attachmentPath = "C:\Users\jensenl5\Documents\WWSCAN_watcher\detections\$date.csv"

# Send an email if detections are found
$from = "youremail@atate.gov" # input sender email
$to = @("doej1@state.gov","doej2@state.gov")  # Use an array for multiple email recipients
$subject = "ALERT: WWSCAN Measles Detection"
$body = "WastewaterSCAN uploaded data on a new MeV detection in Michigan. Please check the attached CSV file for details. Note: This automated email alert system is still being tested, and therefore may not be accurate. Please double check all data."
$smtpServer = "coreosmtp.state.mi.us" # ask your IT department for this

# Send email
Send-MailMessage -From $from -To $to -Subject $subject -Body $body -SmtpServer $smtpServer -Attachments $attachmentPath
