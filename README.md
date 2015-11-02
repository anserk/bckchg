Multi-threading background changer for gnome desktop.
Download images from a subreddit on imgur and store them in an images directory where the other thread is looping on.

IMPORTANT
---------
You have to register on imgur https://api.imgur.com/oauth2/addclient in order to get the client_id and secret_client_id.
You need to copy those key in the auth.ini file.

CONFIGURATION
-------------
You need to set the client_id and client_secret in the auth.ini file. Copy and paste the key you get from the registration url.
Don't put quotes around the key.

RUN
---
To start just run
```
    pip install -r requirements.txt
    python main.py
```
