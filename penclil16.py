#!/usr/bin/env python
# coding: utf-8

# In[0]:


from selenium import webdriver
from bs4 import BeautifulSoup
import os
import lxml

# In[1]

from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)


# In[23]:


website = driver.get('https://www.ilmakiage.co.il/mineral-lip-pencil-4046')


# In[24]:


for _ in range(100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

soup1 = driver.page_source.encode("utf-8")

driver.close()


# In[25]:


soup = BeautifulSoup(soup1, 'lxml')


# In[26]:


if soup.find('span', class_='qtyValidate_color')['style'] == 'display: none;':
    email_val = 'send'
    result = "Tut sheli, it'shopping time, your favorite lip pencil is in stock \n https://www.ilmakiage.co.il/mineral-lip-pencil-4043 \n"
    print(result)
elif soup.find('span', class_='qtyValidate_color')['style'] == 'display: block;':
    email_val = 'not_send'
    result = 'Ooops, the stock is empty. Open the app later to check quantity \n'
    print(result)
else:
    email_val = 'send'
    result = 'Error'
    print(result)


import boto3
if email_val == 'send':
    ses_client = boto3.client("ses", region_name="ap-northeast-1")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
    Destination={
            "ToAddresses": [
                "shuster.landing@gmail.com",
            ],
        },
    Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": result,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Velvet pink color lip pencil is available",
            },
        },
    Source="shuster.landing@gmail.com",
    )
