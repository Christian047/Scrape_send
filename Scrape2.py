# Send email with attachment
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os
import Scrape1 


subject = 'Scraped data'
body = 'Please find attached the data extracted from the website.'
recipient = input('Enter the recipient email address: ')
sender = input('Enter the sender email address: ')
password = input('Enter the sender email password: ')

# Create SMTP session
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login(sender, password)

# Add attachment
attachment = open(Scrape1.excel_file, 'rb')
filename = os.path.basename(Scrape1.excel_file)
attachment_data = attachment.read()
attachment.close()

# Create email message with attachment
message_with_attachment = MIMEMultipart()
message_with_attachment['Subject'] = subject
message_with_attachment['From'] = sender
message_with_attachment['To'] = recipient

# Attach the Excel file
attachment = MIMEApplication(attachment_data, _subtype="xlsx")
attachment.add_header('Content-Disposition', 'attachment', filename=filename)
message_with_attachment.attach(attachment)

# Add body to the email
message_with_attachment.attach(MIMEText(body, 'plain'))

# Send email
smtp.send_message(message_with_attachment)
print('Email sent successfully!')

# Close SMTP session
smtp.quit()