# This program pulls data from TFL APIs and then tweets when the status of tube lines changes
# Written by James Hatch, 2021
# v14 release notes:
# Updated to fix Elizabeth line not working (due to TFL API changing from TFLrail to elizabeth-line)
# Updated to remove the TFL app key from this file and move to jhcreds, to avoid publishing that to GitHub
# Functionality not yet supported includes:
# Handling of multiple statuses per line (e.g. delays on part of the line and part suspended at another)

import tweepy
from datetime import datetime
import pytz
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
import os
import jhcreds
if os.name == 'nt':
    pathtotxtfile = ''
else:
    pathtotxtfile = '/home/pi/jhpythonscripts/'

print (str(datetime.now(pytz.timezone('Europe/London')).strftime("%Y-%m-%d %H:%M:%S")))

# Open the previous JSON response file saved locally:
try:
    with open(pathtotxtfile + 'tfltravelupdates_dataasjson.txt', 'r') as f:
        dataasjson_previous = json.loads(f.read())
except Exception as e:
    print('Error doing json.loads of the previous file; file is probably blank. Last run probably had an error in the TFL API bit')
    print(e)

# Request the new JSON response file from TFL and save it locally, over the previous version:
tflconn = http.client.HTTPSConnection('api.tfl.gov.uk')
tflapp_key = jhcreds.tflapp_key
tflpayload = ''
tflheaders = {}
f = open(pathtotxtfile + 'tfltravelupdates_dataasjson.txt', 'w')
try:
    tflconn.request('GET', '/Line/Mode/tube,dlr,overground,tram,elizabeth-line/Status?app_key=' + tflapp_key, tflpayload, tflheaders)
    dataasjson = json.loads(tflconn.getresponse().read().decode('utf-8'))
    if dataasjson != '':
        f.write(str(json.dumps(dataasjson)))
except Exception as e:
    print('Error in the TFL API bit: ' + str(e))
f.close()

# Twitter API Credentials & Setup
# consumer credentials are the app's credentials. access credentials are the individual twitter account credentials.

consumer_key = jhcreds.consumer_key
consumer_secret = jhcreds.consumer_secret
raspimessengerconsumer_key = jhcreds.raspimessengerconsumer_key
raspimessengerconsumer_secret = jhcreds.raspimessengerconsumer_secret
raspimessengeraccess_key = jhcreds.raspimessengeraccess_key
raspimessengeraccess_secret = jhcreds.raspimessengeraccess_secret

tweettext = ''
oktotweet = 0 # set to 0 to block tweets from actually going out, basically to keep it in dev mode

for index, jsonline in enumerate(dataasjson):

    getattr(jhcreds, jsonline.get('id').replace('-','')).status = jsonline.get('lineStatuses')[0].get('statusSeverityDescription')
    getattr(jhcreds, jsonline.get('id').replace('-','')).prevstatus = dataasjson_previous[index].get('lineStatuses')[0].get('statusSeverityDescription')

    line = getattr(jhcreds, jsonline.get('id').replace('-','')).line
    linename = getattr(jhcreds, jsonline.get('id').replace('-','')).linename
    handle = getattr(jhcreds, jsonline.get('id').replace('-','')).handle
    id = getattr(jhcreds, jsonline.get('id').replace('-','')).id
    access_key = getattr(jhcreds, jsonline.get('id').replace('-','')).access_key
    access_secret = getattr(jhcreds, jsonline.get('id').replace('-','')).access_secret

    status = jsonline.get('lineStatuses')[0].get('statusSeverityDescription')
    prevstatus = dataasjson_previous[index].get('lineStatuses')[0].get('statusSeverityDescription')

    #only bother if the status has actually changed since last time
    if status != prevstatus:
        tweetthisone = 1
        if status == 'Good Service':
            tweettext = ('Good Service has resumed on the ' + linename + ' Line')
            if prevstatus == 'Service Closed' or prevstatus == 'Minor Delays':
                tweetthisone = 0
        elif status == 'Planned Closure':
            tweettext = ('Planned Closure on the ' + linename + ' Line')
            tweettext += ('\nDetails: https://tfl.gov.uk/')
        elif status == 'Minor Delays':
            tweettext = ('Minor Delays on the ' + linename + ' Line')
            tweettext += ('\nDetails: https://tfl.gov.uk/')
            if prevstatus == 'Good Service':
                tweetthisone = 0
        elif status == 'Severe Delays':
            tweettext = ('Severe Delays on the ' + linename + ' Line')
            tweettext += ('\nDetails: https://tfl.gov.uk/')
        elif status == 'Service Closed':
            tweetthisone = 0
        else:
            tweettext = (linename + ' Line status update: ' + status)
            tweettext += ('\nDetails: https://tfl.gov.uk/')
        if oktotweet + tweetthisone == 2:
            print ('Now tweeting: ' + tweettext)
            try:
                if access_key != 'XXXX':
                    auth = tweepy.OAuthHandler(jhcreds.consumer_key, jhcreds.consumer_secret)
                    api = tweepy.API(auth)
                    auth.set_access_token(access_key, access_secret)
                    api.update_status(tweettext + '\n' + str(datetime.now(pytz.timezone('Europe/London')).strftime("%I:%M%p")).lower())
            except Exception as e:
                auth = tweepy.OAuthHandler(raspimessengerconsumer_key, raspimessengerconsumer_secret)
                api = tweepy.API(auth)
                auth.set_access_token(raspimessengeraccess_key, raspimessengeraccess_secret)
                print('Error sending tweet for the ' + linename + ' Line: ' + str(e))
                api.update_status('Error sending tweet for the ' + linename + ' Line: ' + str(e))
        else:
            print ('oktotweet is: ' + str(oktotweet) + '. tweetthisone is: ' + str(tweetthisone) + '. No tweet is being sent. This is what would have been tweeted:')
            print (tweettext)