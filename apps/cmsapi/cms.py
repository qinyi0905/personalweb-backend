from flask import Blueprint, request, current_app, g

import config
from models.user import UserModel
from models.role import Permission, RoleModel
from models.operation import (
    BannerModel,
    AnnounceModel,
    ToolModel,
    ToolTypeModel,
    LinkModel
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from .decorators import permission_required
from .forms import (
    UploadImageForm,
    AddBannerForm,
    AddAnnounceForm,
    AddToolTypeForm,
    AddToolForm,
    AddLinkForm,
    AddUserForm
)
import os, time
from hashlib import md5
from utils import restful
from exts import db
from bs4 import BeautifulSoup
from utils.systeminfo import SystemInfo
from sqlalchemy.sql import func

cmsapi_bp = Blueprint("cmsapi", __name__, url_prefix="/cmsapi")


@cmsapi_bp.before_request
@jwt_required()
def front_before_reuqest():
    if request.method == "OPTIONS":
        return
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(id=identity).first()
    if user:
        setattr(g, "user", user)


def clean_images():
    image_urls = []

    # 收集数据库中的图片URL
    for _ in db.session.query(ToolModel.icon_url).all():
        image_urls.append(_[0])
    for _ in db.session.query(BannerModel.image_url).all():
        image_urls.append(_[0])

    media_root = os.path.join(config.BASE_DIR, "media")
    for root, dirs, files in os.walk(media_root):
        for filename in files:
            file_path = os.path.join(root, filename)
            # 提取相对路径进行比较
            relative_path = os.path.relpath(file_path, media_root).replace("\\", "/")
            # 检查相对路径是否在数据库记录中
            if not any(relative_path in url for url in image_urls):
                os.remove(file_path)


@cmsapi_bp.post("/banner/upload")
@permission_required(Permission.BANNER)
def upload_banner_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image_url = form.image_url.data
        _, ext = os.path.splitext(image_url.filename)
        filename = md5((g.user.username + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)
        image_url.save(image_path)
        return restful.ok(data={"image_url": "/media/banner/" + filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.get("/banner/list")
@permission_required(Permission.BANNER)
def banner_list():
    banners = BannerModel.query.order_by(BannerModel.create_time.desc()).all()
    return restful.ok(data=[banner.to_dict() for banner in banners])


@cmsapi_bp.post("/banner/add")
@permission_required(Permission.BANNER)
def add_banner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        #检查轮播图名称是否已存在
        if BannerModel.query.filter_by(image_url=image_url).first():
            return restful.params_error(message="轮播图已存在")
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url)
        db.session.add(banner)
        db.session.commit()
        return restful.ok(data=banner.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.get("/banner/refresh")
@permission_required(Permission.BANNER)
def refresh_banner():
    image_urls = []
    for _ in db.session.query(BannerModel.image_url).all():
        image_urls.append(_[0])

    for filename in os.listdir(current_app.config['BANNER_IMAGE_SAVE_PATH']):
        if not any(filename in url for url in image_urls):
            image_path = os.path.join(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)
            if os.path.exists(image_path):
                os.remove(image_path)
    return restful.ok()


@cmsapi_bp.post("/banner/delete")
@permission_required(Permission.BANNER)
def delete_banner():
    banner_id = request.form.get("id")
    if not banner_id:
        return restful.params_error(message="参数错误")

    banner = BannerModel.query.get(banner_id)
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="轮播图不存在")


@cmsapi_bp.post("/banner/update")
@permission_required(Permission.BANNER)
def update_banner():
    banner_id = request.form.get("id")
    name = request.form.get("name")
    image_url = request.form.get("image_url")
    link_url = request.form.get("link_url")
    if not all([banner_id, name, image_url, link_url]):
        return restful.params_error(message="参数错误")
    banner = BannerModel.query.get(banner_id)
    if banner:
        banner.name = name
        banner.image_url = image_url
        banner.link_url = link_url
        db.session.commit()
    return restful.ok()


@cmsapi_bp.route("/announce/list")
@permission_required(Permission.ANNOUNCE)
def announce_list():
    page = request.args.get('page', type=int, default=1)
    page_size = current_app.config['PER_PAGE_COUNT']
    start = (page - 1) * page_size
    end = start + page_size
    announce_obj = AnnounceModel.query.order_by(AnnounceModel.create_time.desc())
    total_count = announce_obj.count()
    announces = announce_obj.slice(start, end)
    return restful.ok(
        data={'announce_list': [announce.to_dict() for announce in announces], 'total_count': total_count, 'page': page,
              'pagesize': page_size})


@cmsapi_bp.post("/announce/add")
@permission_required(Permission.ANNOUNCE)
def add_announce():
    form = AddAnnounceForm(request.form)
    if form.validate():
        title = form.title.data
        content = form.content.data
        text_muted = BeautifulSoup(content, "html.parser").text[:25] + "..."
        author_id = g.user.id
        announce = AnnounceModel(title=title, content=content, text_muted=text_muted, author_id=author_id)
        db.session.add(announce)
        db.session.commit()
        return restful.ok(data=announce.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.post("/announce/delete")
@permission_required(Permission.ANNOUNCE)
def delete_announce():
    announce_id = request.form.get("id")
    if not announce_id:
        return restful.params_error(message="参数错误")
    announce = AnnounceModel.query.get(announce_id)
    if announce:
        db.session.delete(announce)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="公告不存在")


@cmsapi_bp.post("/announce/active")
@permission_required(Permission.ANNOUNCE)
def announce_active():
    is_active = request.form.get("is_active")
    announce_id = request.form.get("id")
    announce = AnnounceModel.query.get(announce_id)
    announce.is_active = True if is_active == "1" else False
    db.session.commit()
    return restful.ok(data=announce.to_dict())


@cmsapi_bp.get("/tooltype/list")
@permission_required(Permission.TOOL)
def tooltype_list():
    tooltypes = ToolTypeModel.query.order_by(ToolTypeModel.priority.desc()).all()
    return restful.ok(data=[tooltype.to_dict() for tooltype in tooltypes])


@cmsapi_bp.post("/tooltype/add")
@permission_required(Permission.TOOL)
def add_tooltype():
    form = AddToolTypeForm(request.form)
    if form.validate():
        name = form.name.data
        priority = form.priority.data
        icon = form.icon.data
        #检查数据是否存在
        if ToolTypeModel.query.filter(ToolTypeModel.name == name).first():
            return restful.params_error(message="工具分类已存在")
        tooltype = ToolTypeModel(name=name, priority=priority, icon=icon)
        db.session.add(tooltype)
        db.session.commit()
        return restful.ok(data=tooltype.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.post("/tooltype/delete")
@permission_required(Permission.TOOL)
def delete_tooltype():
    tooltype_id = request.form.get("id")
    if not tooltype_id:
        return restful.params_error(message="参数错误")

    tooltype = ToolTypeModel.query.get(tooltype_id)
    if tooltype:
        db.session.delete(tooltype)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="工具分类不存在")


@cmsapi_bp.get("/tool/list")
@permission_required(Permission.TOOL)
def tool_list():
    page = request.args.get('page', type=int, default=1)
    page_size = current_app.config['PER_PAGE_COUNT']
    start = (page - 1) * page_size
    end = start + page_size
    tool_obj = ToolModel.query.order_by(ToolModel.create_time.desc())
    total_count = tool_obj.count()
    tools = tool_obj.slice(start, end)
    return restful.ok(
        data={'tool_list': [tool.to_dict() for tool in tools], 'total_count': total_count, 'page': page,
              'pagesize': page_size})


@cmsapi_bp.post("/tool/add")
@permission_required(Permission.TOOL)
def add_tool():
    form = AddToolForm(request.form)
    if form.validate():
        name = form.name.data
        description = form.description.data
        icon_url = form.icon_url.data
        link_url = form.link_url.data
        type_name = form.type_name.data
        type_id = ToolTypeModel.query.filter(ToolTypeModel.name == type_name).first().id
        #检查数据是否存在
        if ToolModel.query.filter(ToolModel.name == name).first() or ToolModel.query.filter(ToolTypeModel.link_url == link_url):
            return restful.params_error(message="工具已存在")
        tool = ToolModel(name=name, description=description, icon_url=icon_url, link_url=link_url, type_id=type_id)
        db.session.add(tool)
        db.session.commit()
        return restful.ok(data=tool.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.post("/tool/delete")
@permission_required(Permission.TOOL)
def delete_tool():
    tool_id = request.form.get("id")
    if not tool_id:
        return restful.params_error(message="参数错误")

    tool = ToolModel.query.get(tool_id)
    if tool:
        db.session.delete(tool)
        db.session.commit()
        clean_images()
        return restful.ok()
    else:
        return restful.params_error(message="工具不存在")


@cmsapi_bp.post("/tool/update")
@permission_required(Permission.TOOL)
def update_tool():
    tool_id = request.form.get("id")
    name = request.form.get("name")
    icon_url = request.form.get("icon_url")
    link_url = request.form.get("link_url")
    description = request.form.get("description")
    type_name = request.form.get("type_name")
    if not all([tool_id, name, icon_url, link_url, description, type_name]):
        return restful.params_error(message="参数错误")
    tool = ToolModel.query.get(tool_id)
    if tool:
        tool.name = name
        tool.icon_url = icon_url
        tool.link_url = link_url
        tool.description = description
        tool.type_id = ToolTypeModel.query.filter(ToolTypeModel.name == type_name).first().id
        db.session.commit()
        clean_images()
    return restful.ok()


@cmsapi_bp.post("/tool/icon/upload")
@permission_required(Permission.TOOL)
def upload_tool_icon():
    form = UploadImageForm(request.files)
    if form.validate():
        icon_url = form.icon_url.data
        _, ext = os.path.splitext(icon_url.filename)
        filename = md5((g.user.username + str(time.time())).encode("utf-8")).hexdigest() + ext
        icon_path = os.path.join(current_app.config['TOOL_ICON_SAVE_PATH'], filename)
        icon_url.save(icon_path)
        return restful.ok(data={"icon_url": "/media/tool/icon/" + filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.post("/link/add")
@permission_required(Permission.LINK)
def add_link():
    form = AddLinkForm(request.form)
    if form.validate():
        name = form.name.data
        link_url = form.link_url.data
        #检查链接是否已经存在
        if LinkModel.query.filter(LinkModel.link_url == link_url).first():
            return restful.params_error(message="链接已经存在")
        link = LinkModel(name=name, link_url=link_url)
        db.session.add(link)
        db.session.commit()
        return restful.ok(data=link.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.get("/link/list")
@permission_required(Permission.LINK)
def link_list():
    page = request.args.get('page', type=int, default=1)
    page_size = current_app.config['PER_PAGE_COUNT']
    start = (page - 1) * page_size
    end = start + page_size
    link_obj = LinkModel.query.order_by(LinkModel.create_time.desc())
    total_count = link_obj.count()
    links = link_obj.slice(start, end)
    return restful.ok(
        data={'link_list': [link.to_dict() for link in links], 'total_count': total_count, 'page': page,
              'pagesize': page_size})


@cmsapi_bp.post("/link/delete")
@permission_required(Permission.LINK)
def delete_link():
    link_id = request.form.get("id")
    if not link_id:
        return restful.params_error(message="参数错误")

    link = LinkModel.query.get(link_id)
    if link:
        db.session.delete(link)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="链接不存在")


@cmsapi_bp.post("/link/update")
@permission_required(Permission.LINK)
def update_link():
    link_id = request.form.get("id")
    name = request.form.get("name")
    link_url = request.form.get("link_url")
    if not all([link_id, name, link_url]):
        return restful.params_error(message="参数错误")
    link = LinkModel.query.get(link_id)
    if link:
        link.name = name
        link.link_url = link_url
        db.session.commit()
    return restful.ok()


@cmsapi_bp.post("/link/deploy/status")
@permission_required(Permission.LINK)
def deploy_link_status():
    link_id = request.form.get("id")
    is_deployed = request.form.get("is_deployed")
    if not link_id:
        return restful.params_error(message="参数错误")

    link = LinkModel.query.get(link_id)
    if not link:
        return restful.params_error(message="链接不存在")
    link.is_deployed = True if is_deployed == "1" else False
    db.session.commit()
    return restful.ok(data=link.to_dict())


@cmsapi_bp.get("/user/list")
@permission_required(Permission.USER)
def user_list():
    page = request.args.get('page', type=int, default=1)
    page_size = current_app.config['PER_PAGE_COUNT']
    start = (page - 1) * page_size
    end = start + page_size
    user_obj = UserModel.query.join(RoleModel).order_by(RoleModel.permissions.desc(),UserModel.join_time)
    total_count = user_obj.count()
    users = user_obj.slice(start, end)
    user_list = [user.to_dict() for user in users]
    return restful.ok(
        data={'user_list': user_list, 'total_count': total_count, 'page': page,
              'pagesize': page_size})


@cmsapi_bp.post("/user/active")
@permission_required(Permission.USER)
def active_user():
    is_active = request.form.get('is_active', type=int)
    user_id = request.form.get("id")
    user = UserModel.query.get(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok(data=user.to_dict())


@cmsapi_bp.post("/user/delete")
@permission_required(Permission.USER)
def delete_user():
    user_id = request.form.get("id")
    if not user_id:
        return restful.params_error(message="参数错误")
    user = UserModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="用户不存在")


@cmsapi_bp.post("/user/update")
@permission_required(Permission.USER)
def update_user():
    user_id = request.form.get("id")


@cmsapi_bp.post("/user/add")
@permission_required(Permission.USER)
def add_user():
    form = AddUserForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        realname = form.realname.data
        role_id = form.role_id.data
        role = RoleModel.query.get(role_id)
        if not role:
            return restful.params_error(message="角色不存在")
        #检查用户名是否已经存在
        if UserModel.query.filter_by(username=username).first():
            return restful.params_error(message="用户名已经存在")
        user = UserModel(username=username, password=password, realname=realname, role=role)
        db.session.add(user)
        db.session.commit()
        return restful.ok(data=user.to_dict())
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@cmsapi_bp.post("/user/update/role")
@permission_required(Permission.USER)
def update_user_role():
    user_id = request.form.get("id")
    role_id = request.form.get("role_id")
    user = UserModel.query.get(user_id)
    role = RoleModel.query.get(role_id)
    if not all([user, role]):
        return restful.params_error(message="参数错误")
    if user:
        user.role_id = role_id
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message="用户不存在")

@cmsapi_bp.get("/sys/useage")
def sys_useage():
    systeminfo = SystemInfo()
    get_cpu_usage = systeminfo.get_cpu_usage()
    get_mem_usage = systeminfo.get_memory_usage()
    return restful.ok(data={"cpu_usage": get_cpu_usage, "mem_usage": get_mem_usage})

@cmsapi_bp.get("/tool/menu")
def tool_menu():
    result = db.session.query(ToolTypeModel.name,func.count(ToolTypeModel.name)).join(ToolModel).group_by(ToolModel.type_id).all()
    data=[]
    for _ in result:
        data.append({'name': _[0],'value': _[1]})
    return restful.ok(data=data)

@cmsapi_bp.get("/tool/usage/count")
def tool_usage_count():
    xAxis_data = []
    yAxis_data = []
    for _ in db.session.query(ToolModel.name,ToolModel.access_count).order_by(ToolModel.access_count.desc()).all()[:8]:
        xAxis_data.append(_[0])
        yAxis_data.append(_[1])
    return restful.ok(data={'xAxis_data': xAxis_data, 'yAxis_data': yAxis_data})

@cmsapi_bp.get("/web/access/info")
def web_access_info():
    systeminfo = SystemInfo()
    date_access = systeminfo.get_nginx_access_log()
    xAxis_data = []
    yAxis_data = []
    for key,value in date_access.items():
        xAxis_data.append(key)
        yAxis_data.append(value)
    return restful.ok(data={'xAxis_data': xAxis_data, 'yAxis_data': yAxis_data})
