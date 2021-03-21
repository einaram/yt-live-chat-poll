# yt-live-chat-poll


**Proof of concept/prototype**

Let youtube live chat viewers vote with free text answers and generates a bar chart that can be inserted into Open Broadcast Studio (OBS). 
Kept up to date when inserted as an image slideshow.

Vote by   

    !VOTENAME 
    
Does some simple corrections to match misspelled words.


 # Usage
 1. Find your youtube live chat ID by taking your stream id from the streaming url:
    https://studio.youtube.com/channel/{STREAMID}/livestreaming
 2. Get a Youtube API key
 2. Get the chat ID from the youtube API 
    https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list?apix=true&apix_params=%7B%22part%22%3A%5B%22snippet%22%5D%2C%22id%22%3A%5B%22STREAM_URL_ID%22%5D%7D
 3. Rename config.sample.py to config.py
 4. Insert Chat ID and your youtube API key into config.py
 4. Run yt.py and insert image into OBS

 
 
