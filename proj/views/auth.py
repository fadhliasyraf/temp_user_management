from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *


bp_auth = Blueprint('bp_auth', __name__)



@bp_auth.route('/register_user', methods=['POST'])
def register_user():
    response = dict(code='111', data=dict(), description="User registered successfully", status="OK")
    try:
        params = request.form['ref']
        params = json.loads(params)
        print(params)
        print(response)

        newUser = User()


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_auth.route('/login', methods=['POST'])
def login():
    response = dict(code='111', data=dict(), description="Logged in successfully", status="OK")
    try:
        params = request.form['ref']
        params = json.loads(params)
        print(params)
        print(response)


        result = dict()
        result["usernameStatus"] = False
        result["passwordStatus"] = False
        # ph = PasswordHasher()
        # uc = UserAccount.query.filter(UserAccount.isDeleted == False).all()
        user_id = ""

        uc = User.query.filter(User.username == params["username"], User.isDeleted == False).first()

        # if uc:
        #     result["usernameStatus"] = True
        #     if ph.verify(uc.password, param['password']):
        #         result["passwordStatus"] = True
        #         user_id = uc.user_profile_id

        result["user_id"] = user_id

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)