from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/update_user', methods=['POST'])
def update_user():
    response = dict(code='111', data=list(), description="User updated successfully", status="OK")
    try:
        params = request.form['ref']
        params = json.loads(params)
        print(params)

        updatedUser = User.query.filter(User.uuid == params["uuid"], User.isDeleted == False).first()

        if not updatedUser:
            raise Exception("User does not exist.")

        updatedUser.name = params["name"]
        updatedUser.rank = params["rank"]
        updatedUser.role = params["role"]
        updatedUser.username = params["username"]
        updatedUser.password = params["password"]

        db.session.commit()


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)


@bp_user.route('/register_user', methods=['POST'])
def register_user():
    response = dict(code='111', data=dict(), description="User registered successfully", status="OK")
    try:
        params = request.form['ref']
        params = json.loads(params)
        print(params)
        print(response)

        newUser = User(
            params["name"],
            params["rank"],
            params["role"],
            params["username"],
            params["password"],
        )

        db.session.add(newUser)
        db.session.commit()


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_user.route('/user_list', methods=['GET'])
def user_list():
    response = dict(code='111', data=list(), description="User registered successfully", status="OK")
    try:

        allUsers = User.query.all()

        for user in allUsers:
            print(user)
            objUser = func.convert(user)

            del objUser["username"]
            del objUser["password"]

            response["data"].append(objUser)


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)
