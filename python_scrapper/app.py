#!/usr/bin/python3

from flask import Flask, request, send_from_directory
import subprocess
from pymongo import MongoClient
from config import *
from utils import *
import re

app = Flask(__name__, static_url_path='/home/qet/SCRAPER/python_scrapper/client')

conx = get_mongo_client()
db = get_db_name(conx)

#APIs

@app.route('/events')
def get_events():
    '''
    FUTURE UPDATES:
    1. Add support for multiple field search
    '''
    args = request.args
    search_by = None
    search_keyword = None
    if "searchBy" in args:
        search_by = args["searchBy"]
    if "searchKeyword" in args:
        search_keyword = args["searchKeyword"]

    if search_by and search_keyword:
        cnd1 = re.compile(f".*"+ search_keyword +".*", re.I)
        result = json_friendly(list(db.events.find({search_by: {'$regex': cnd1}})))
    else:
        result = json_friendly(list(db.events.find()))
    return {"events": result}



@app.route('/<path:path>')
def root(path):
    print("paht>", path)
    return send_from_directory('client', path)
