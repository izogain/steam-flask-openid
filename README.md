# Steam OpenID on Google app engine.

Demo app using Valve Steam OpenID authentication. The app uses Flask and basic openID libraires.
A demo of the application can be found a this location : [gaesteamopenid.appspot.com](https://gaesteamopenid.appspot.com)


## Installation

`git clone https://github.com/izogain/steam-flask-openid`

`cd steam-flask-openid`

Make sure you installed the required SDKs by following the instructions on [Google app engine](https://cloud.google.com/appengine/docs/python/quickstart)

Open the run.py file and add a random secret key for Flask and your steam API key. Steam API key can be registered on [Valve website](https://steamcommunity.com/dev/apikey).

Then, you must install the required libraries in the root lib folder:

`pip install -t lib/ -r requirements.txt`

Testing locally :

`dev_appserver.py --host=0.0.0.0 --admin_host=0.0.0.0 app.yaml`


## Deployment

Using Gloud:

`gcloud app deploy --version=<app version> --project=<project id >`

`gcloud preview datastore create-indexes index.yaml --project=<project id>`

Using appcfg:

`appcfg.py update app`

`appcfg.py update_indexes ../steam-flask-openid/`

> The appcfg method requires adding the version, project ID and the module values to the app.yam file :
> - application: project_id
> - version: version
> - module: default

Updating the indexes is theoretically only required during the first deploy or during a change to the index.yaml file.

## Common Error
In case of 500 error during deployment, its mostly due to the datastore indexes, it takes a few minutes for google to serve them. Make sure to update indexes and check the datastore admin interface in Google cloud console, as well as the error logs.


## Implementation

OpenID requires the use of a database to store state during the authentication phase. This app uses Google datastore using a simple implementation of the OpenID Store Interface. The
Implementation can be found in the root directory as gaeopenidstore.py (extracted from the library [peterhudec/authomatic](https://github.com/peterhudec/authomatic)).
Once the app verified the user through openID and successfully logged in for the first time, an entry is added to the google datastore using a key with the format :
**steam:md5(steam_id)** (provider:md5(provider id)).
You may choose another way, like a mysql database for users. Quite frankly my understanding of google datastore is quite limited, i wish it was as simple as dynamoDb...

## Flask
Flask is eazy to use, i highly recommend checking out [Miguel Grinberg](https://github.com/miguelgrinberg) github page for examples of applications.

Simple example of sign in with openID : [Sign in with Steam ID](http://flask.pocoo.org/snippets/42/)
