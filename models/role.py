from exts import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Permission(object):
    # 255的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR =        0b00000001
    # 2. 管理用户权限
    USER =         0b00000010
    # 3. 管理轮播图的权限
    BANNER =      0b00000100
    # 4. 管理工具的权限
    TOOL =        0b00001000
    # 5. 管理公告的权限
    ANNOUNCE =      0b00010000
    # 6. 管理Github链接的权限
    LINK =        0b00100000



class RoleModel(db.Model, SerializerMixin):
    serialize_only = ("id", "name", "desc", "create_time", "permissions")
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=Permission.VISITOR)