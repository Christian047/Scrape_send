from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import requests
import re    
import pandas as pd
import smtplib
import os


# Define website URL
url = input("Enter the website URL: ")
site = f"https://www.{url}"

# Request website content
response = requests.get(site)
website_content = response.text

# Extract links
links = re.findall(r'<a\s+.?href=[\'"](.?)[\'"].*?>', website_content)

# Extract phone numbers
phone_numbers = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", website_content)

# Extract emails
emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', website_content)

# Ensure all arrays have the same length
data_length = min(len(links), len(phone_numbers), len(emails))
links = links[:data_length]
phone_numbers = phone_numbers[:data_length]
emails = emails[:data_length]

# Save data as Excel file
data = {'Links': links, 'Phone Numbers': phone_numbers, 'Emails': emails}
df = pd.DataFrame(data)
excel_file = 'Scraped.xlsx'
df.to_excel(excel_file, index=False)
print('exraction successful')

# Send email with attachment
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
attachment = open(excel_file, 'rb')
filename = os.path.basename(excel_file)
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