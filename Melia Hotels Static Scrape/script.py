import requests
from requests.structures import CaseInsensitiveDict
import csv
#Function to find all hotels

print("Don't type file extension")
name = input("Enter the name you want to give your extracted file: ")
name = str(name)
name = name.strip()
name = f"{name}.csv"
def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                if isinstance(d, dict):
                    for result in find(key, d):
                        yield result
#Root URL
url = "https://www.melia.com/rest/hotels/destinations-tree?lang=en"   
#Headers                     
headers = CaseInsensitiveDict()
headers["Connection"] = "keep-alive"
headers["sec-ch-ua"] = "' Not;A Brand';v='99', 'Google Chrome';v='91', 'Chromium';v='91'"
headers["Accept"] = "*/*"
headers["X-Requested-With"] = "XMLHttpRequest"
headers["sec-ch-ua-mobile"] = "?0"
headers["Sec-Fetch-Site"] = "same-origin"
headers["Sec-Fetch-Mode"] = "cors"
headers["Sec-Fetch-Dest"] = "empty"
headers["Referer"] = "https://www.melia.com/en/hotels/germany/munster/home.htm"

#Sending Response
resp = requests.get(url, headers=headers)
#Getting data in JSON
data = resp.json()

#Finding all hotels in JSON
print("FINDING HOTELS INFO ...")
csv_list = []
for searchedData in data["searchData"]:
    hotels = list(find("hotels",searchedData))
    hotels = list(filter(None, hotels))
    for hotel in hotels:
        for hot in hotel:
            csv_list.append([hot['lat'],hot['lon'],"MELIA",hot['title'],"Melia Lux Chain"])
        
#Writing CSV
print("WRITING CSV FILE ...")
with open(name, 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['LAT',"LON","COMPANY","LOCATION NAME","LOCATION TYPE"])
    writer.writerows(csv_list)
print("FILE SAVED SUCCESSFULLY ...")

