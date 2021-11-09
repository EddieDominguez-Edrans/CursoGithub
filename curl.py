#!/usr/bin/python

import signalfx
import requests
import subprocess
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
httplist = '/etc/signalfx/scripts/httplist'

def get_http_status(url, line_count):
    try:
        a = requests.Session()
        a.max_redirects = 5
        r = a.get(url, verify=False)
        print("%s %s %s" % (line_count, r.url, r.status_code))
        tosfx(r.status_code, url)
    except requests.exceptions.ConnectionError:
        print("%s Error %s" % (line_count, url))
        tosfx(0, url)
    except requests.exceptions.TooManyRedirects:
        print("%s Error %s" % (line_count, url))
        tosfx(302, url)
        
def geturl(fname):
    line_count = 0
    with open(fname) as f:
        for line in f.readlines():
            line_count += 1
            get_http_status(line.strip(), line_count)
            #print(line)
def tosfx(code, url):
    with signalfx.SignalFx(ingest_endpoint='https://ingest.us1.signalfx.com').ingest('B9T-2fvZ9j8k3gbJXNl1IQ') as sfx:
        try:
            sfx.send(
                gauges=[
                    {
                        "metric": "HTTPCheck",
                        "value": int(code),
                        "dimensions": {
                            "url": url
                        }
                    }
                ]
            )
#Quality QA
#            print("sfx send " + str(errorcount) + " " + site)
        finally:
            sfx.stop()

# - - MAIN - - #

geturl(httplist)