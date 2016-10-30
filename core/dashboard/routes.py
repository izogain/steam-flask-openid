from flask import Flask, render_template, g, redirect
from . import dashboard
from ..auth import login_required
from ..auth.providers import get_steam_userinfo

@dashboard.route("/")
@login_required
def index():
    steamdata = get_steam_userinfo(g.user.id_provider)
    return render_template('index.html', nickname=g.user.nickname, id_provider=g.user.id_provider,steamdata=steamdata)
