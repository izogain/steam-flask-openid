from flask import json,current_app

from ..models import User
from google.appengine.api import users
from google.appengine.ext import ndb



import re
import hashlib
import urllib, urllib2

STEAM="steam"

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')


#returns a datastore key with the format : provider:md5(id_user), ex: steam:md5(17458415145)
def parent_key_provider(provider,provider_id):
    return ndb.Key(provider, hashlib.md5(provider_id).hexdigest())

#checks if the user already exist in the datastore, if not create a new one
def get_or_create(provider,id_provider):
    parent = parent_key_provider(provider,id_provider)
    rv = User.query(User.id_provider==id_provider, ancestor=parent).get()

    if rv is None :
        if provider == STEAM :
            return get_or_create_steam(id_provider, parent)
    return rv

#create an entree for the new user
#it does an http request to steam API to retrieve the user name, you may want to move that
#to a later stage to avoid http request failures in the middle of authentification
def get_or_create_steam(id_provider, parent):
    usr = User(parent=parent)
    steamdata = get_steam_userinfo(id_provider) #api request to steam
    usr.nickname = steamdata['personaname']
    usr.id_provider = id_provider
    key = usr.put()
    usr.key = key
    return usr

##########if request for STEAM API Fails , make sure to catch urlib exception and display appropriate error
def get_steam_userinfo(steam_id):
    options = {
        'key': current_app.config['STEAM_KEY'],
        'steamids': steam_id
    }
    url = 'http://api.steampowered.com/ISteamUser/' \
          'GetPlayerSummaries/v0002/?%s' % urllib.urlencode(options)
    rv = json.load(urllib2.urlopen(url))
    return rv['response']['players'][0] or {}
