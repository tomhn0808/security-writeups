import base64
import subprocess
import re
import requests

from bs4 import BeautifulSoup


s = requests.Session()
url = "http://mywebsite.com/captcha_page"
response = s.get(url)
if response.status_code in [200]:
    html = response.text
else:
    print ('Could not retrieve: %s, err: %s - status code: %s' % 
           (url, response.text, response.status_code))
    html = None

# 1. Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# 2. Find the <img> tag
img_tag = soup.find('img')

# 3. Get the 'src' attribute
src_data = img_tag['src']

# 4. The 'src' contains a prefix: "data:image/png;base64,"
#    We need to split it at the comma and take the second part [1].
base64_string = src_data.split(',')[1]

png_data = base64.b64decode(base64_string)

with open("captcha.png", "wb") as f:
    f.write(png_data)

# Use gocr to resolve the captcha
resolved_captcha = subprocess.check_output("gocr -i captcha.png", stderr=subprocess.STDOUT, shell=True,text=True) 
#shell=True for running in terminal, text=True to get string output

resolved_captcha = re.sub(r'[^A-Za-z0-9]', '', resolved_captcha).strip()
print("Resolved Captcha:", resolved_captcha)

# Prepare data for POST request
data={'cametu': resolved_captcha}
post_response = s.post(url, data=data)
post_response.raise_for_status()
print("POST Response:", post_response.text)
