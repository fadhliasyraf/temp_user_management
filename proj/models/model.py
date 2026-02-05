import uuid
from flask import json
from proj.models import db


class User(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(200))
    rank = db.Column(db.String(200))
    role = db.Column(db.String(200))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, rank, role, username, password):
        self.uuid = uuid.uuid4().hex
        self.name = name
        self.rank = rank
        self.role = role
        self.username = username
        self.password = password
