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


@bp_message.route('/get_new_messages/<string:role>/<int:index>', methods=['GET'])
def get_new_messages(role, index):
    response = dict(code='111', data=dict(), description="New messages retrieved successfully", status="OK")
    try:
        # Query messages where to_user matches the role and id is greater than the provided index
        new_messages = Message.query.filter(
            Message.to_user == role,
            Message.id > index,
            Message.isDeleted == None
        ).order_by(Message.id.asc()).all()

        # Convert messages to dictionary format
        messages_list = [
            {
                'id': msg.id,
                'from_user': msg.from_user,
                'to_user': msg.to_user,
                'type': msg.type,
                'message': msg.message,
                'date_created': msg.date_created.strftime('%d-%m-%Y %H:%M:%S') if msg.date_created else None
            }
            for msg in new_messages
        ]

        response['data'] = {'messages': messages_list, 'count': len(messages_list)}

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)