from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os

from dash import Dash
import dash_bootstrap_components as dbc

external_scripts=[
    {'src': 'https://cdn.tailwindcss.com'}
]
server=Flask(__name__)
CORS(server,supports_credentials=True)

app=Dash(
    __name__,
    server=server,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    external_scripts=external_scripts,
    url_base_pathname="/app/"
)
app.scripts.config.serve_locally=True

server.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///transactdb.db"
server.config['SECRET_KEY']="SUPER_SECRET_KEY"
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
server.config["JWT_COOKIE_SECURE"] = False
server.config["JWT_SECRET_KEY"] = "super-secret"
server.config['JWT_COOKIE_CSRF_PROTECT']=False
server.config['JWT_ACCESS_COOKIE_PATH'] = '/'
server.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies", "json", "query_string"]


db=SQLAlchemy(server)
jwt=JWTManager(server)