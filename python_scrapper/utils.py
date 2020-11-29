from pymongo import MongoClient
from config import *
import datetime


def get_mongo_client():
    return MongoClient(MONGO_DB_IP, MONGO_DB_PORT, fsync=True)

def get_db_name(conx):
    return conx[DB_NAME]

def json_friendly(obj):
    if not obj or type(obj) in (int, float, str, bool):
        return obj
    if type(obj) == datetime.datetime:
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    if type(obj) == dict:
        for k in obj:
            obj[k] = json_friendly(obj[k])
        return obj
    if type(obj) == list:
        for i, v in enumerate(obj):
            obj[i] = json_friendly(v)
        return obj
    if type(obj) == tuple:
        temp = []
        for v in obj:
            temp.append(json_friendly(v))
        return tuple(temp)
    return str(obj)

