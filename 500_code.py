#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
import csv
from bs4 import BeautifulSoup


# In[10]:


ur="https://internshala.com/internships/page-"


# In[11]:


from collections import defaultdict
dict=defaultdict(list)
def fun(dict,url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    container=soup.find("div",class_="detail_view")
    title=container.find("span",class_="profile_on_detail_page").text
    company=container.find("a", class_="link_display_like_text").text.strip()
    url=container.find("a",href=True, class_="link_display_like_text")
    url="https://internshala.com/"+url["href"]
    location=container.find("a",class_="location_link").text
    start=container.find("span",class_="start_immediately_desktop")
    if start:
        start=container.find("span",class_="start_immediately_desktop").text.strip()
    else:
        start=container.find("div",id="start-date-first").text.strip()
    duration=container.find_all("div",class_="item_body")[1].text.strip()
    stipend=container.find_all("div",class_="item_body")[2].text.strip()
    job_type=container.find("div", class_="label_container label_container_desktop").text.strip()
    
    applications=container.find("div",class_="applications_message")
    if applications:
        applications=container.find("div",class_="applications_message").text.strip()
    
    web=soup.find("div",class_="text-container website_link")
    website=""
    if web:
        website=web.find("a",href=True)["href"]
    dict["job_title"].append(title)
    dict["company_name"].append(company)
    dict["URL"].append(url)
    dict["start_time"].append(start)
    #dict["last_date_to_apply"].append()
    dict["Duration"].append(duration)
    dict["Location"].append(location)
    dict["Job"].append(job_type)
    dict["applications"].append(applications)
    dict["company_website"].append(website)
    


# In[12]:


for _ in range(1,14):
    url=ur+str(_)
    print(_)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    a_tags=soup.find_all("div",class_="heading_4_5 profile")
    for i in a_tags:
        url="https://internshala.com/"+i.find("a")["href"]
        fun(dict,url)
print(len(dict["Job"]))
print(dict["Location"])
print(len(dict["Location"]))
    


# In[13]:



for j,i in enumerate(dict["start_time"]):
    if i=="Immediately":
        dict["end_time"].append(" ")
        continue
    else:
        flag=True
        date=i.split("-")
        if len(date)==2:
            d,m,y=date[1].split()
            if m=="Jun'":
                m="June"
            elif m=="Jul'":
                m="July"
            elif m[:3]=="Aug'":
                m="August"
            else:
                m="September"
            i=m+" "+d+","+"20"+y
            dict["end_time"].append(i)
            s_d,s_m=date[0].split()
            if s_m=="Jun":
                s_m="June"
            elif s_m=="Jul":
                s_m="July"
            elif s_m[:3]=="Aug":
                s_m="August"
            else:
                s_m="September"
            new=s_m+" "+s_d+","+"2021"
            dict['start_time'][j]=new
        else:
            d,m,y=date[0].split()
            if m=="Jun'":
                m="June"
            elif m=="Jul'":
                m="July"
            elif m[:3]=="Aug":
                m="August"
                
            else:
                m="September"
            i=m+" "+d+","+"20"+y
            dict["start_time"][j]=i
            dict["end_time"].append(" ")
            


# In[14]:


import pandas as pd
new = pd.DataFrame(dict)
print(dict["end_time"])


# In[15]:


new.shape
nlist=list(new.columns)
print(nlist)
new_l=[]
for i in range(0,4):
    new_l.append(nlist[i])
new_l.append(nlist[-1])
for i in range(4,9):
    new_l.append(nlist[i])
print(new_l)
new=new[new_l]


# In[16]:


new.head(40)


# In[17]:


new.to_csv("result_out.csv",encoding="utf-8",index=False)


# In[ ]:




