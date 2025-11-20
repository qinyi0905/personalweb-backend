from flask import Blueprint, render_template, request, make_response

from .forms import LoginForm
from models.user import UserModel
from models.role import RoleModel, Permission
from models.operation import BannerModel, AnnounceModel, ToolModel
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO
import time
from exts import db, cache
from flask_jwt_extended import create_access_token

index_bp = Blueprint('index', __name__, url_prefix='/')


@index_bp.route('/')
def index():
    list_tools = []

    banners = BannerModel.query.order_by(BannerModel.create_time).all()
    announces = AnnounceModel.query.order_by(AnnounceModel.create_time.desc()).all()
    tools = ToolModel.query.order_by(ToolModel.create_time).all()
    for tool in tools:
        if (tool.to_dict())['name'].lower() in ['Mindoc'.lower(), 'Linux Command'.lower(), 'IT-TOOLS'.lower(),
                                                'Quick Reference'.lower()]:
            list_tools.append(tool.to_dict())
    list_announces = [announce.to_dict() for announce in announces][:2]
    context = {
        "banners": banners,
        "announces": list_announces,
        "tools": list_tools
    }
    return render_template('front/index.html', **context)


@index_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                return restful.params_error("用户名或密码错误！")
            if not user.check_password(password):
                return restful.params_error("用户名或密码错误！")
            if not user.is_active:
                return restful.permission_error()
            token = create_access_token(identity=user.id)
            permissions = []
            for attr in dir(Permission):
                if not attr.startswith("_"):
                    permission = getattr(Permission, attr)
                    if user.has_permission(permission):
                        permissions.append(attr.lower())

            user_dict = user.to_dict()
            user_dict['permissions'] = permissions
            return restful.ok(data={"token": token, "user": user_dict})
        else:
            return restful.params_error(message=form.messages[0])


@index_bp.route("/graph/captcha")
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    key = md5((captcha + str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key, captcha)
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    resp.set_cookie("_graph_captcha_key", key, max_age=3600)
    return resp


@index_bp.route('/cms')
def cms():
    return render_template('cms/index.html')
