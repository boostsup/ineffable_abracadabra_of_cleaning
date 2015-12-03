# encoding: utf-8
import similarize

from w2v_api import w2v_api
import threading
from twitter import *
import yaml
from time import sleep
from datetime import datetime
import os
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-d", "--daemonize", action="store_true", dest="daemonize",
                  help="run forever, tweet at 10am and 4pm",)
(options, args) = parser.parse_args()

def api_thread():
    w2v_api.run()

#start the API
threads = []
t = threading.Thread(target=api_thread)
t.daemon = True
threads.append(t)
t.start()

#once the API is started, get twitter creds, generate a joke, tweet it, then sleep
current_dir = os.path.dirname(__file__)
twitter_creds_filename = os.path.join(current_dir, 'twitter_creds.secret')
with open(twitter_creds_filename, 'r') as f:
  creds = yaml.load(f)
  twitter = Twitter(auth=OAuth(creds["token"], creds["secret"], creds["consumer_key"], creds["consumer_secret"]))

def tweet():
  joke = similarize.do()
  if len(joke) < 140:
    twitter.statuses.update(status=joke)

if options.daemonize:
  while True:
    now  = datetime.now()
    print("what time is it? it's %i:%i" % (now.hour, now.minute))
    if (now.hour == 10 or now.hour == 16) and now.minute >= 0 and now.minute < 10:
      tweet()
    sleep(60 * 10) # check the time every ten minutes
else:
  tweet()
