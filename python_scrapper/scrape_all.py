#!/usr/bin/python3

import threading
import subprocess
from utils import *
import techmeme_scraper
import computerworld_scraper

if __name__ == '__main__':
    t1 = threading.Thread(target=techmeme_scraper.fetch_events_json, args=(True,))
    t2 = threading.Thread(target=computerworld_scraper.fetch_events_json, args=(True,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
