from apps.cmsapi.decorators import permission_required
from models.user import UserModel
from models.role import RoleModel, Permission
from exts import db



def init_roles():
    # 普通用户
    visitor_role = RoleModel(name="普通用户", desc="仅能访问首页",
                              permissions=Permission.VISITOR)
    # 网站管理员
    admin_role = RoleModel(name="网站管理员", desc="负责整个网站的管理",
                           permissions=Permission.USER | Permission.BANNER | Permission.TOOL | Permission.LINK | Permission.ANNOUNCE)
    # 轮播图和工具管理员
    tool_admin_role = RoleModel(name="工具管理员", desc="负责工具和轮播图的管理",permissions=Permission.BANNER | Permission.TOOL| Permission.LINK)

    #公告管理员
    announce_admin_role = RoleModel(name="公告管理员", desc="负责公告的管理",permissions=Permission.ANNOUNCE)

    # 开发者（权限是最大的，仅一个用户）
    developer_role = RoleModel(name="超级管理员", desc="负责网站的开发", permissions=Permission.ALL_PERMISSION)

    db.session.add_all([developer_role, announce_admin_role, tool_admin_role, admin_role, visitor_role])
    db.session.commit()
    print("角色添加成功！")

def init_admin_user():
    role = RoleModel.query.filter_by(name="超级管理员").first()
    user = UserModel(username="admin", password='Ericsson_1@', realname='超级管理员', role=role)
    db.session.add(user)
    db.session.commit()
    print('超级管理员用户创建成功！')