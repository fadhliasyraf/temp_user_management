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
