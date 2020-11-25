from  dateutil.parser import isoparse
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator


import difflib
import requests
import datetime
import time
import config
#CONFIG
# #
LIVECHATID = config.LIVECHATID
YOUR_API_KEY = config.YOUR_API_KEY
pollid = config.pollid

def append_last_msgs(results, last_timestamp):    
    # Get channelID here: 
    # https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
    # channelId = "tIIX4_oE27U"

    baseurl = f"https://youtube.googleapis.com/youtube/v3/liveChat/messages?liveChatId={LIVECHATID}&part=snippet&key={YOUR_API_KEY}"
    if not last_timestamp:
        last_timestamp = datetime.datetime.utcnow()
        last_timestamp= last_timestamp.replace(tzinfo=datetime.timezone.utc)
        print("Starting timestamp", last_timestamp)
        # last_timestamp = datetime.datetime(2020, 11, 23, 10, 10, tzinfo=datetime.timezone.utc)
    timestamps= [last_timestamp]

    resp = requests.get(baseurl)
    if not resp.status_code == 200:
        print(resp)
        exit
    msgs = resp.json()
    print("msg count",len(msgs['items']))   

    
    for msg in msgs["items"]:
        timestamp =isoparse(msg['snippet']['publishedAt'])
        if timestamp > last_timestamp: 

            timestamps.append(timestamp)
            if msg['kind'] == 'youtube#liveChatMessage':
                msg_text = msg['snippet']['displayMessage']
                if msg_text.startswith("!"):
                    msg_text = msg_text.lstrip('!')
                    
                    # Find similar votes and add them to the same key:
                    matches = [x for x in results.keys() if  difflib.SequenceMatcher(None, msg_text, x).ratio() > 0.75]
                    if matches:
                        msg_text = matches[0]
                    if results.get(msg_text):
                        results[msg_text] += 1
                    else:
                        results[msg_text] = 1
            
    return results, max(timestamps)
    # nextpage_token = "t&pageToken=GPS5obmDnO0...."


results = {}
last_timestamp = None
def create_barplot(results):
    plt.figure(figsize=(4,10))
    plt.barh(range(len(results)), results.values(), align='center')
    plt.yticks(range(len(results)), list(results.keys()))

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.tight_layout()
    plt.savefig(f"images/poll/{pollid}.png")
    plt.close()
while True:
    results, last_timestamp = append_last_msgs(results, last_timestamp)
    create_barplot(results)
    print(results)
    time.sleep(2)

# plt.show()
