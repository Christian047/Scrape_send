import requests
import re
import pandas as pd

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