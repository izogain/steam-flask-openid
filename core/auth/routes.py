from flask import Flask, render_template, request, g, session, json, redirect

from ..models import User
from . import auth
from .. import oid

from .providers import _steam_id_re , get_or_create, get_steam_userinfo, STEAM, parent_key_provider

from google.appengine.api import users


@auth.route('/auth')
def index():
    if g.user is not None:
        return redirect('/')
    else:
        return render_template('login.html')

@auth.route("/auth/steam")
@oid.loginhandler
def login_steam():
    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login("http://steamcommunity.com/openid")

@auth.route('/auth/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@auth.before_app_request
def before_request():
    g.user = None
    if 'user_id' in session and 'provider' in session:
        parent = parent_key_provider(session['provider'], session['user_id'])
        g.user = User.query(User.id_provider==session['user_id'], ancestor=parent).get()

@oid.after_login
def new_steam_user(resp):
    match = _steam_id_re.search(resp.identity_url)
    g.user = get_or_create(STEAM, match.group(1))
    session['user_id'] = g.user.id_provider
    session['provider'] = STEAM
    return redirect(oid.get_next_url())
