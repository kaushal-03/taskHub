from celery import Celery
from pymongo import MongoClient
import requests

app = Celery('celery_init', broker='pyamqp://')

@app.task
def Task(sender, forwardTo):
    try:
       client = MongoClient('mongodb://localhost:27017')
       db = client['celeryConnect']
       collection = db['mobileDeviceConfig']
    #    collection.insert_one({"sender":sender, "forwardTo":forwardTo})
       data = collection.find_one({"email": { "$eq": "test@gmail.com" }})
       print(data["FCMToken"])
      
    except Exception as error:
        print(error) 

@app.task
def AutomateDispatch(data):
    try:
        client = MongoClient('mongodb://localhost:27017')
        db = client['celeryConnect']
        collection = db['celeryConnect']
        FCMCollection = db['mobileDeviceConfig']
        collection.insert_one({"message": data, "status": "latest"})
        params = {"startHistoryId":data}
        headers = {"Authorization": "Bearer "}
        r = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
        if r.status_code == 200:
            response = r.json()
            loggedInUser = response["email"]
            print("logged in user", loggedInUser)
            r = requests.get("https://gmail.googleapis.com/gmail/v1/users/me/history", params=params, headers=headers)
            response=r.json()
            if r.status_code == 200:
                message_id = response['history'][0]['messages'][0]['id']
                r = requests.get(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}", headers=headers)
                response=r.json()
                headersData = response["payload"]["headers"]
                message = {
                    "sound": 'default',
                    "title": 'Message from your email assistant!',
                    "body": 'You recieved a mail from the selected sender.',
                } 
                for h in headersData:
                    if h['name'] == "From":
                        if loggedInUser in h['value']:
                            data = FCMCollection.find_one({"email": { "$eq": "test@gmail.com" }})
                            payload = {
                                **message,
                                "to":data["FCMToken"]
                            }
                            r = requests.post('https://exp.host/--/api/v2/push/send', payload)
                            print(r)
                            print("yes")
                        else:
                            print("No")
        else:
            print("Unauthorized User")
    except Exception as error:
        print("exception", error)





