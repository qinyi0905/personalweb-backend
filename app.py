from flask import Flask

import config
from exts import db, cache, csrf, jwt, cors
from flask_migrate import Migrate

from apps.front.index import index_bp
from apps.front.announce import announce_bp
from apps.front.tool import tool_bp
from apps.front.link import link_bp
from apps.cmsapi.cms import cmsapi_bp
from apps.media.media import media_bp
import commands
from models import user

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
cache.init_app(app)
csrf.init_app(app)
jwt.init_app(app)
cors.init_app(app, resources={r"/cmsapi/*": {"origins": "*"}})

# 排除csrf验证
csrf.exempt(cmsapi_bp)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(index_bp)
app.register_blueprint(cmsapi_bp)
app.register_blueprint(media_bp)
app.register_blueprint(announce_bp)
app.register_blueprint(tool_bp)
app.register_blueprint(link_bp)

# 注册命令
app.cli.command("init_roles")(commands.init_roles)
app.cli.command("init_admin_user")(commands.init_admin_user)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
