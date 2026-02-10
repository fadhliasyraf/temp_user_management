import uuid
from flask import json
from pwdlib import PasswordHash

from proj.models import db
from sqlalchemy import event

user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_uuid',
        db.String(32),
        db.ForeignKey('user.uuid', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'role_id',
        db.String(32),
        db.ForeignKey('role.uuid', ondelete='CASCADE'),
        primary_key=True
    )
)



class User(db.Model):
    uuid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(200))
    rank_uuid = db.Column(
        db.String(32),
        db.ForeignKey('rank.uuid'),
        nullable=True
    )
    username = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    auth_token = db.Column(db.String(32),nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.Boolean, nullable=False, default=False)

    rank = db.relationship(
        'Rank',
        lazy='joined'
    )

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        passive_deletes=True,
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    def __init__(self, name, rank_uuid, username, password):
        self.uuid = uuid.uuid4().hex
        self.name = name
        self.rank_uuid = rank_uuid
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




@event.listens_for(db.metadata, 'after_create')
def create_default_user(*args, **kwargs):
    # Default ranks
    default_ranks = [
        ('ADMIN', 'Admin'),
        ('MAJOR', 'Major'),
        ('CAPTAIN', 'Captain'),
        ('SARGEANT', 'Sargeant')
    ]

    for code, name in default_ranks:
        if not Rank.query.filter_by(code=code).first():
            db.session.add(Rank(code, name))

    # Default roles
    default_roles = [
        ('ADMIN', 'Admin'),
        ('Weapon Controller', 'Weapon Controller'),
        ('Warfare Director', 'Warfare Director'),
        ('Picture Controller', 'Picture Controller'),
        ('Maintenance', 'Maintainer')
    ]

    for code, name in default_roles:
        if not Role.query.filter_by(code=code).first():
            db.session.add(Role(code, name))

    db.session.commit()

    # Default admin user
    if not User.query.filter_by(username='admin').first():
        pwd_hasher = PasswordHash.recommended()
        hashed_password = pwd_hasher.hash('admin')

        selectedRank = Rank.query.filter_by(code="ADMIN").first()
        selectedRole = Role.query.filter_by(code="ADMIN").first()

        default_user = User(
            name='System Admin',
            rank_uuid=selectedRank.uuid,
            username='admin',
            password=hashed_password
        )
        default_user.roles.append(selectedRole)

        db.session.add(default_user)
        db.session.commit()
        print("Default admin user created")


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    from_user = db.Column(db.String(255), nullable=False, index=True)
    to_user = db.Column(db.String(255), nullable=False, index=True)
    type = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    isDeleted = db.Column(db.DateTime, nullable=True)

    def __init__(self, from_user, to_user, type, message):
        self.from_user = from_user
        self.to_user = to_user
        self.type = type
        self.message = message

