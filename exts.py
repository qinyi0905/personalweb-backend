from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
cache = Cache()
csrf = CSRFProtect()
jwt = JWTManager()
cors = CORS()

