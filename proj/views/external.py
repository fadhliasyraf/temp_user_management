from flask import Blueprint, request ,jsonify
from proj.models.model import *
from proj.views import func
from pwdlib import PasswordHash

bp_external = Blueprint('bp_external', __name__)


@bp_external.route('/update_password', methods=['POST'])
def update_password():
    response = dict(code='111', data=dict(), description="User password updated successfully", status="OK")
    try:
        params = request.get_json()
        print(params)

        pwd_hasher = PasswordHash.recommended()

        user = User.query.filter(User.auth_token == params["token"], User.isDeleted == False).first()
        if not user:
            raise Exception("Incorrect token.")

        if user:
            if pwd_hasher.verify(params['old_password'], user.password):
                hashedPassword = pwd_hasher.hash(params['new_password'])
                user.password = hashedPassword
            else:
                raise Exception("Old password not matched.")


        db.session.commit()

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_external.route('/get_profile', methods=['POST'])
def get_profile():
    response = dict(code='111', data=dict(), description="User profile fetched successfully", status="OK")
    try:
        params = request.get_json()
        print(params)

        userProfile = User.query.filter(User.auth_token == params["token"], User.isDeleted == False).first()

        if userProfile:
            objUser = func.convert(userProfile)
            # del objUser["username"]
            del objUser["password"]
            del objUser["auth_token"]

            response["data"] = objUser


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)



@bp_external.route('/user_authentication', methods=['POST'])
def user_authentication():
    response = dict(code='111', data=dict(), description="Logged in successfully", status="OK")
    try:
        params = request.get_json()
        print(params)

        pwd_hasher = PasswordHash.recommended()

        userLogin = User.query.filter(User.username == params["username"], User.isDeleted == False).first()
        if not userLogin:
            raise Exception("Authentication failed. Incorrect Credentials.")

        if userLogin:
            if pwd_hasher.verify(params['password'], userLogin.password):
                pass
            else:
                raise Exception("Authentication failed. Incorrect Credentials.")

        if 'role' in params:
            if params["role"]:
                has_role = any(role.code == params["role"] for role in userLogin.roles)
                if not has_role:
                    raise Exception("Authentication failed. User don't have this role.")
            else:
                raise Exception("Authentication failed. Role is missing.")
        else:
            raise Exception("Authentication failed. Role is missing.")

        tokenGenerated = uuid.uuid4().hex
        userLogin.auth_token = tokenGenerated

        db.session.commit()

        response["data"]["token"] = userLogin.auth_token


    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)


