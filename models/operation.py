# models/operation.py

from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin


class BannerModel(db.Model, SerializerMixin):
    serialize_only = ('id', 'name', 'image_url', 'link_url', 'create_time')
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class AnnounceModel(db.Model, SerializerMixin):
    serialize_only = ('id', 'title', 'text_muted', 'content', 'create_time', 'is_active', 'access_count', 'author')
    __tablename__ = 'announce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    text_muted = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    access_count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"))

    author = db.relationship("UserModel", backref=db.backref("announces"))


class ToolModel(db.Model, SerializerMixin):
    serialize_only = ('id', 'name', 'description', 'icon_url', 'link_url', 'create_time', 'type')
    __tablename__ = 'tool'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
    access_count = db.Column(db.Integer, default=0)

    type = db.relationship("ToolTypeModel", backref=db.backref("types"))


class ToolTypeModel(db.Model, SerializerMixin):
    serialize_only = ('id', 'name', 'priority', 'icon', 'create_time')
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class LinkModel(db.Model, SerializerMixin):
    serialize_only = ('id', 'name', 'link_url', 'create_time', 'is_deployed')
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    is_deployed = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
