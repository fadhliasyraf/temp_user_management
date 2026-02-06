from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func
from pwdlib import PasswordHash



bp_auth = Blueprint('bp_auth', __name__)




@bp_auth.route('/user_authentication', methods=['POST'])
def user_authentication():
    response = dict(code='111', data=dict(), description="Logged in successfully", status="OK")
    try:
        params = request.get_json()
        print(params)


        result = dict()

        pwd_hasher = PasswordHash.recommended()

        userLogin = User.query.filter(User.username == params["username"], User.isDeleted == False).first()
        if not userLogin:
            raise Exception("Authentication failed. Incorrect Credentials.")

        if userLogin:
            result["usernameStatus"] = True
            if pwd_hasher.verify(params['password'], userLogin.password):
                pass
            else:
                raise Exception("Authentication failed. Incorrect Credentials.")

        if 'role' in params:
            if params["role"]:
                # do something
                print(params["role"])
                pass
            else:
                raise Exception("Authentication failed. Role is missing.")
        else:
            raise Exception("Authentication failed. Role is missing.")

        tokenGenerated = uuid.uuid4().hex
        userLogin.token = tokenGenerated

        db.session.commit()

        response["data"]["token"] = userLogin.token


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)


@bp_auth.route('/admin_login', methods=['POST'])
def admin_login():
    response = dict(code='111', data=dict(), description="Logged in successfully", status="OK")
    try:
        params = request.get_json()
        print(params)


        result = dict()

        pwd_hasher = PasswordHash.recommended()

        userLogin = User.query.filter(User.username == params["username"], User.isDeleted == False).first()
        if not userLogin:
            raise Exception("Login failed. Incorrect Credentials.")

        if userLogin:
            result["usernameStatus"] = True
            if pwd_hasher.verify(params['password'], userLogin.password):
                pass
            else:
                raise Exception("Login failed. Incorrect Credentials.")

        has_admin = any(role.code == "ADMIN" for role in userLogin.roles)


        if not has_admin:
            raise Exception("Login failed. Only admin allowed.")


        objUser = func.convert(userLogin)

        del objUser["username"]
        del objUser["password"]

        response["data"] = objUser

        tokenGenerated = uuid.uuid4().hex
        userLogin.token = tokenGenerated
        db.session.commit()

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)