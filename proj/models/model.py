import uuid
from flask import json
from proj.models import db

user_roles = db.Table(
    'user_roles',
    db.Column('user_uuid', db.String(32), db.ForeignKey('user.uuid'), primary_key=True),
    db.Column('role_id', db.String(32), db.ForeignKey('role.uuid'), primary_key=True)
)


class User(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(200))
    rank = db.Column(db.String(200))
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    def __init__(self, name, rank, username, password):
        self.uuid = uuid.uuid4().hex
        self.name = name
        self.rank = rank
        self.username = username
        self.password = password


class Role(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)  # e.g. ADMIN, DOCTOR
    name = db.Column(db.String(200))  # Human readable
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, code, name):
        self.uuid = uuid.uuid4().hex
        self.code = code
        self.name = name


class Rank(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)  # e.g. ADMIN, DOCTOR
    name = db.Column(db.String(200))  # Human readable
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, code, name):
        self.uuid = uuid.uuid4().hex
        self.code = code
        self.name = name



