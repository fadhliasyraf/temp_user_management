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


@bp_message.route('/get_message/<user_role>', methods=['GET'])
def get_message(user_role):
    response = dict(code='111', data=dict(), description="Message retrieved successfully", status="OK")
    try:
        messages = Message.query.filter_by(to_user=user_role, isDeleted=None).all()

        messages_list = [{
            'id': msg.id,
            'from_user': msg.from_user,
            'to_user': msg.to_user,
            'message_type': msg.type,
            'message': msg.message,
            'date_created': msg.date_created.strftime('%d/%m/%Y %H:%M:%S') if msg.date_created else None
        } for msg in messages]

        response['data'] = messages_list

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)