from flask import Blueprint, render_template, request, make_response, jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func
from pwdlib import PasswordHash

bp_lov = Blueprint('bp_lov', __name__)


@bp_lov.route('/get_ranks', methods=['GET'])
def get_ranks():
    response = dict(code='111', data=list(), description="Ranks retrieved successfully", status="OK")
    try:
        all_ranks = Rank.query.filter(Rank.isDeleted == False).all()

        # Serialize the ranks data
        ranks_data = []
        for rank in all_ranks:
            ranks_data.append({
                'uuid': rank.uuid,
                'code': rank.code,
                'name': rank.name
            })

        response['data'] = ranks_data

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data=[], description=str(msg), status="FAILED")

    return jsonify(response)


@bp_lov.route('/get_roles', methods=['GET'])
def get_roles():
    response = dict(code='111', data=list(), description="Roles retrieved successfully", status="OK")
    try:
        all_roles = Role.query.filter(Role.isDeleted == False).all()

        # Serialize the roles data
        roles_data = []
        for role in all_roles:
            roles_data.append({
                'uuid': role.uuid,
                'code': role.code,
                'name': role.name
            })

        response['data'] = roles_data

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data=[], description=str(msg), status="FAILED")

    return jsonify(response)
