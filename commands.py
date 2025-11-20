from models.user import UserModel
from models.role import RoleModel, Permission
from exts import db


def init_roles():
    roles_data = [
        {"name": "普通用户", "desc": "仅能访问首页", "permissions": Permission.VISITOR},
        {"name": "网站管理员", "desc": "负责整个网站的管理","permissions": Permission.USER | Permission.BANNER | Permission.TOOL | Permission.LINK | Permission.ANNOUNCE},
        {"name": "工具管理员", "desc": "负责工具和轮播图的管理","permissions": Permission.BANNER | Permission.TOOL | Permission.LINK},
        {"name": "公告管理员", "desc": "负责公告的管理", "permissions": Permission.ANNOUNCE},
        {"name": "超级管理员", "desc": "负责网站的开发", "permissions": Permission.ALL_PERMISSION}
    ]

    for role_data in roles_data:
        # 检查角色是否已存在
        existing_role = RoleModel.query.filter_by(name=role_data["name"]).first()
        if not existing_role:
            role = RoleModel(**role_data)
            db.session.add(role)
        else:
            print(f"{role_data['name']}角色已存在！")

    db.session.commit()
    print("角色初始化完成！")

def init_admin_user():
    role = RoleModel.query.filter_by(name="超级管理员").first()
    if UserModel.query.filter_by(username="admin").first():
        print('超级管理员用户已存在！')
        return
    user = UserModel(username="admin", password='Ericsson_1@', realname='超级管理员', role=role)
    db.session.add(user)
    db.session.commit()
    print('超级管理员用户创建成功！')