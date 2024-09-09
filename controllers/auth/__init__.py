from flask import Blueprint,jsonify,request,session,g,make_response,current_app
from models import User,UserSession
from config import db,jwt
from constants.https_status_codes import *
from utils.ApiError import ApiError
from utils.ApiResponse import ApiResponse

auth=Blueprint("auth",__name__,url_prefix="/api/v1/auth")

# USERNMAE="mridulti"

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

    if checked_user and checked_user.password==data['password']:

        resp = make_response(jsonify({"user":checked_user.to_json()}))
        
        user_session= UserSession(username=checked_user.username)
        db.session.add(user_session)
        db.session.commit()
        return resp
    return ApiError("Invalid credentials", HTTP_400_BAD_REQUEST)
    

@auth.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users]), 200

@auth.route("/current-username",methods=['GET'])
def get_current_user():
    user=UserSession.query.first_or_404().username
    return jsonify({"user":user})

@auth.route("/logout", methods=['GET','POST'])
def logout():
    user=UserSession.query.first_or_404()
    db.session.delete(user)
    db.session.commit()
    resp = make_response(ApiResponse("User Logged Out", HTTP_200_OK))
    return resp