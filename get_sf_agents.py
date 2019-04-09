import requests
from bs4 import BeautifulSoup
import csv
import time

start = time.time()
result = requests.get("https://www.compass.com/sitemaps/agents/sf/")
src = result.content
soup = BeautifulSoup(src, "lxml")

urls = soup.find_all("loc")[1:]

# print(len(urls))
agents = []

for i in range(len(urls)):
    try:
        url2 = urls[i].text
        result2 = requests.get(url2)
        src2 = result2.content
        soup2 = BeautifulSoup(src2, "lxml")

        phone_div = soup2.find_all("div", class_="agents1506-profile-cardPhone")
        phone = phone_div[0].find("a").text.replace("M:", "").strip()
        if phone == ".." and len(phone_div) > 1:
            phone = phone_div[1].find("a").text.replace("O:", "").strip()

        if len(soup2.text.split("sales: [")) > 1:
            sales = soup2.text.split("sales: [")[1].split("rentals:")[0]

            address_list = soup2.text.split("prettyAddress")

            if len(sales.split('"neighborhood":')) > 1:
                city_list = sales.split('"neighborhood":')
            else:
                city_list = sales.split('"city":')

            price_list = sales.split("lastKnown")

            if len(city_list) > 1:
                price_1 = price_list[1].split(', "')[0][3:-2].replace(".", "")
                price_1 = price_1[:-3] + "." + price_1[-3:]
                price_1 = price_1[:-7] + "." + price_1[-7:]
                price_1 = "$" + price_1
            else:
                price_1 = ""

            if len(city_list) > 2:
                price_2 = price_list[2].split(', "')[0][3:-2].replace(".", "")
                price_2 = price_2[:-3] + "." + price_2[-3:]
                price_2 = price_2[:-7] + "." + price_2[-7:]
                price_2 = "$" + price_2
            else:
                price_2 = ""

            if len(city_list) > 3:
                price_3 = price_list[3].split(', "')[0][3:-2].replace(".", "")
                price_3 = price_3[:-3] + "." + price_3[-3:]
                price_3 = price_3[:-7] + "." + price_3[-7:]
                price_3 = "$" + price_3
            else:
                price_3 = ""

            agents.append({
                "agents_name": soup2.find("span", class_="breadcrumbs-currentPage").text.strip(),
                "email": soup2.find("div", class_="agents1506-profile-cardEmail").find("a").text.strip(),
                "phone": phone,
                "office": "San Francisco",
                "link": url2,
                "property_1_address": address_list[1].split('", "')[0][4:] if len(city_list) > 1 else "",
                "property_1_city": city_list[1].split('", "')[0][2:] if len(city_list) > 1 else "",
                "property_1_price": price_1,
                "property_2_address": address_list[2].split('", "')[0][4:] if len(city_list) > 2 else "",
                "property_2_city": city_list[2].split('", "')[0][2:] if len(city_list) > 2 else "",
                "property_2_price": price_2,
                "property_3_address": address_list[3].split('", "')[0][4:] if len(city_list) > 3 else "",
                "property_3_city": city_list[3].split('", "')[0][2:] if len(city_list) > 3 else "",
                "property_3_price": price_3
            })
        else:
            agents.append({
                "agents_name": soup2.find("span", class_="breadcrumbs-currentPage").text.strip(),
                "email": soup2.find("div", class_="agents1506-profile-cardEmail").find("a").text.strip(),
                "phone": phone,
                "office": "San Francisco",
                "link": url2,
                "property_1_address": "",
                "property_1_city": "",
                "property_1_price": "",
                "property_2_address": "",
                "property_2_city": "",
                "property_2_price": "",
                "property_3_address": "",
                "property_3_city": "",
                "property_3_price": ""
            })
    except IndexError as err:
        print(err)
        print(i)
        print(url2)

    time.sleep(3)


with open("sf_agents.csv", "w", encoding='utf8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=agents[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(agents)

end = time.time()
print(end - start)
