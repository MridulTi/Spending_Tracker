from flask import Blueprint,jsonify,request,session,redirect
from models import User
from config import db
from utils.RenderResponse import RenderResponse
from constants.https_status_codes import *
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse

auth=Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.route("/",methods=['GET'])
def index():
    return jsonify("Working!")

@auth.route('/register', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(first_name=data['firstname'],last_name=data['lastname'], username=data['username'], email=data['email'],password=data['password'])
    if not new_user:
        return ApiError("User not created",HTTP_400_BAD_REQUEST)
    db.session.add(new_user)
    db.session.commit()
    return ApiResponse("User Registerd!",HTTP_200_OK,new_user.to_json())

@auth.route("/login",methods=['POST'])
def login():
    data=request.json
    checked_user=User.query.filter_by(email=data['email']).first()
    if not checked_user:
        return ApiError("User not Found",HTTP_400_BAD_REQUEST)
    if checked_user.password==data['password']:
        return ApiResponse("User Loggedin",HTTP_200_OK,checked_user.to_json())

@auth.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users]), 200