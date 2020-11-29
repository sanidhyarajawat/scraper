#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
from utils import *
import sys

'''
FUTURE UPDATES:
1. Check if the event is present in collection, if not then insert
'''

def fetch_events_json(remove_and_insert):
    #Get mongo connection
    conx = get_mongo_client()
    db = get_db_name(conx)

    #URL
    url = "https://www.techmeme.com/events"
    page = urlopen(url)
    html = page.read().decode("utf-8")

    #Read html and find title
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")

    #Finding all divs with class 'rhov'
    table = soup.find_all("div", attrs={"class": "rhov"})

    events = []

    '''
    If single_row has more/indefinite items then store single_row in a list and
    iterate over that list outside of the main loop to reduce the complexity
    '''

    for row in table:
        single_event = {}
        single_row = row.find_all("div")
        #single_row list has 3 items fixed, so directly accessing using index
        single_event["event_name"] = single_row[1].text
        single_event["event_date"] = single_row[0].text
        single_event["location"] = single_row[2].text
        single_event["title"] = title.text
        single_event["website_url"] = url
        events.append(single_event)

    #Insert into mongo events collection
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

