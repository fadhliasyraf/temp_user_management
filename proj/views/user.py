from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func
from pwdlib import PasswordHash

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/delete_user', methods=['POST'])
def delete_user():
    response = dict(code='111', data=dict(), description="User deleted successfully", status="OK")
    try:
        params = request.get_json()

        userProfile = User.query.filter(User.uuid == params["uuid"], User.isDeleted == False).first()

        if userProfile:
            userProfile.isDeleted = True

        db.session.commit()

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_user.route('/get_profile', methods=['POST'])
def get_profile():
    response = dict(code='111', data=dict(), description="User profile fetched successfully", status="OK")
    try:
        uuidParam = request.get_json()

        userProfile = User.query.filter(User.uuid == uuidParam, User.isDeleted == False).first()

        if userProfile:
            objUser = func.convert(userProfile)
            # del objUser["username"]
            del objUser["password"]

            response["data"] = objUser


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_user.route('/get_user_count', methods=['GET'])
def get_user_count():
    response = dict(code='111', data='', description="User count fetched successfully", status="OK")
    try:

        allUsersCount = User.query.count()


        response["data"] = allUsersCount


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_user.route('/update_user', methods=['POST'])
def update_user():
    response = dict(code='111', data=list(), description="User updated successfully", status="OK")
    try:
        params = request.get_json()
        print(params)

        updatedUser = User.query.filter(User.uuid == params["uuid"], User.isDeleted == False).first()

        if not updatedUser:
            raise Exception("User does not exist.")

        role = [role['value'] for role in params['role']]
        role = Role.query.filter(Role.uuid.in_(role)).all()
        updatedUser.username = params["username"]
        updatedUser.name = params["name"]
        updatedUser.rank_uuid = params["rank"]['value']
        updatedUser.roles = role

        if all(param in params for param in ['password', 'confirmPassword']) and params['password'] == params['confirmPassword'] and len(params['password']) != 0:
            pwd_hasher = PasswordHash.recommended()
            hashedPassword = pwd_hasher.hash(params['password'])
            updatedUser.password = hashedPassword

        db.session.commit()


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)


@bp_user.route('/register_user', methods=['POST'])
def register_user():
    response = dict(code='111', data=dict(), description="User registered successfully", status="OK")
    try:
        params = request.get_json()
        print(params)
        pwd_hasher = PasswordHash.recommended()
        hashedPassword = pwd_hasher.hash(params['password'])


        newUser = User(
            params["name"],
            params["rank"],
            # params["role"],
            params["username"],
            hashedPassword,
        )

        for i in params["role"]:
            selectedRole = Role.query.filter_by(uuid=i).first()

            newUser.roles.append(selectedRole)

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

        allUsers = User.query.filter(User.isDeleted == False).all()

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
