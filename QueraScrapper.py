# a scraper that scrapes https://quera.org/magnet/jobs and say which skills are required more than others

# first import requests and BeautifulSoup to get the html of the page and parse it

import requests
from bs4 import BeautifulSoup

# import time to wait 0.5 seconds between each page to not get banned from Quera :(
import time

# spans with "css-1ljl88f" and "css-1suxakh" classes are the ones that contain the skills
skills_dic = {}
stop_it = True

# get_skills function gets the skills of a page and add them to skills_dic
def get_skills(url):
    global skills_dic
    global stop_it


    # if requests spend more than 3 seconds retry it
    while True:
        try:
            page = requests.get(url, timeout=3)
            break
        except:
            print("retrying...")
            continue

    soup = BeautifulSoup(page.content, 'html.parser')

    # if we have a p with text "فرصت شغلی با این مشخصات یافت نشد" it means there is no more pages
    if soup.find('p', text='فرصت شغلی با این مشخصات یافت نشد'):
        stop_it = False
    skills = soup.find_all('span', class_=['css-1ljl88f', 'css-1suxakh'])
    # add skills to skills_dic ( if the skill is already in skills_dic, increase the value by 1 and if not, add it to skills_dic )
    for skill in skills:
        if skill.text in skills_dic:
            skills_dic[skill.text] += 1
        else:
            skills_dic[skill.text] = 1
    

i = 1
# if stop_it is True, it means there is more pages and if it is False, it means there is no more pages
while stop_it:
    # end loop when there is no more pages
    get_skills('https://quera.org/magnet/jobs?page=' + str(i))
    
    # print i to see the progress and user dont bored :D
    print("Page Cursor :" + str(i))
    i += 1
    # wait 0.5 seconds to not get banned
    time.sleep(0.5)
    
print("Done! Results: \n \n")

# show top 10 skills
print("Top 10 skills are:")
for skill in sorted(skills_dic, key=skills_dic.get, reverse=True)[:10]:
    print(skill + " : " + str(skills_dic[skill]))


