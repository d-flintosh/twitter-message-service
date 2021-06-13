*General Overview*
* This cloud function is listening on PubSub topic `twitter-message-service-pubsub`
* The `entrypoint` is in `main.py`
* An attribute, `school` should be attached to each message to denote which school is being triggered
* Credentials are pulled from Google Secret Manager
* An additional message is sent to the main publish account @001Automation

*To Add new Schools*
* Sign Up For A GMail account
* Sign Up For A Twitter account  
* Run the `main` of `twitter_auth.py` to authorize `sports-message-service` to post on that account's behalf
* Take the access token key and access token secret to the Google Secret Manager dictionary of permissions