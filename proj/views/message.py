from datetime import datetime

from flask import Blueprint, request, jsonify
from proj.models.model import *

bp_message = Blueprint('bp_message', __name__)


@bp_message.route('/send_message', methods=['POST'])
def send_message():
    response = dict(code='111', data=dict(), description="Message sent successfully", status="OK")
    try:
        params = request.get_json()
        print(params)

        required_fields = ["from_role", "to_role", "type", "message"]

        for i in required_fields:
            if not params[i]:
                raise Exception("Required values missing.")


        createdMsg = Message(
            params["from_role"],
            params["to_role"],
            params["type"],
            params["message"],
        )

        db.session.add(createdMsg)
        db.session.commit()

    except Exception as e:
        msg = str(e)
        print(msg)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)


@bp_message.route('/delete_message', methods=['DELETE'])
def delete_message():
    response = dict(code='111', data=dict(), description="Message deleted successfully", status="OK")
    try:
        data = request.get_json()
        message_id = data.get('id')

        if not message_id:
            response = dict(code='000', data='', description="Message ID is required", status="FAILED")
            return jsonify(response)

        # Find the message
        message = Message.query.filter_by(id=message_id, isDeleted=None).first()

        if not message:
            response = dict(code='000', data='', description="Message not found or already deleted", status="FAILED")
            return jsonify(response)

        # Soft delete by setting current timestamp
        message.isDeleted = datetime.now()
        db.session.commit()

    except Exception as e:
        db.session.rollback()
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
                'message_type': msg.type,
                'message': msg.message,
                'date_created': msg.date_created.strftime('%d/%m/%Y %H:%M:%S') if msg.date_created else None
            }
            for msg in new_messages
        ]

        response['data'] = messages_list

    except Exception as e:
        msg = str(e)
        response = dict(code='000', data='', description=str(msg), status="FAILED")

    return jsonify(response)