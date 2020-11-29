#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import *

'''
FUTURE UPDATES:
1. Check if the event is present in collection, if not then insert
'''

def fetch_events_json(remove_and_insert):
    #Get mongo connection
    conx = get_mongo_client()
    db = get_db_name(conx)

    #URL
    url = "https://www.computerworld.com/article/3313417/tech-event-calendar-2020-upcoming-shows-conferences-and-it-expos.html"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    #Read html and title
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")

    events = []
    
    #find table tag with given id and all rows inside it
    table = soup.find("table", attrs={"id": "cwsearchabletable"}).tbody.find_all("tr")

    for row in table:
        all_td = row.find_all("td")
        #There are total 4 td currently so using index to fetch data
        #If indefinite td are present then loop over all_td to fetch the result
        data = {}
        data["event_name"] = row.th.a.text
        data["event_date"] = str(all_td[1].text) + " - " + str(all_td[2].text)
        data["location"] = all_td[3].text
        data["title"] = title.text
        data["website_url"] = url
        events.append(data)

    #Insert into Mongo events collection
    if remove_and_insert:
        #Remove the existing data
        db.events.remove({"website_url": url})
        #Insert into mongo events collection
        db.events.insert_many(events)
    else:
        #Insert into mongo events collection
        db.events.insert_many(events)
    return events, url


if __name__ == '__main__':
    remove_and_insert = True

    events_list, url = fetch_events_json(remove_and_insert)

