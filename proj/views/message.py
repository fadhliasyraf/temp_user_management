from flask import Blueprint, render_template, request, make_response,jsonify
import sys, os, json
from proj.models.model import *
from proj.views import func


bp_message = Blueprint('bp_message', __name__)


@bp_message.route('/send_message', methods=['POST'])
def send_message():
    response = dict(code='111', data=dict(), description="Message sent successfully", status="OK")
    try:
        pass

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)

