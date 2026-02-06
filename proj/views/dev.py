from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func
from pwdlib import PasswordHash

bp_dev = Blueprint('bp_dev', __name__)


@bp_dev.route('/inject_role_lov', methods=['POST'])
def inject_role_lov():
    response = dict(code='111', data=dict(), description="Role injected successfully", status="OK")
    try:
        role1 = Role('ADMIN', 'Admin')
        role2 = Role('MAINTENANCE', 'Maintenance')
        role3 = Role('WAROFFICE', 'War Office')

        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)

        db.session.commit()

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

@bp_dev.route('/inject_rank_lov', methods=['POST'])
def inject_rank_lov():
    response = dict(code='111', data=dict(), description="Rank injected successfully", status="OK")
    try:
        rank1 = Rank('MAJOR', 'Major')
        rank2 = Rank('CAPTAIN', 'Captain')
        rank3 = Rank('SARGEANT', 'Sargeant')

        db.session.add(rank1)
        db.session.add(rank2)
        db.session.add(rank3)

        db.session.commit()

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

