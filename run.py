from core import create_app

#update those values
app = create_app(config_name= dict(SECRET_KEY="put a complex random string here",
                                    STEAM_KEY="<your steam api key"))
