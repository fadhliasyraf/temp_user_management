from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func

bp_user = Blueprint('bp_user', __name__)


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
