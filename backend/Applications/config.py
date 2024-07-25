# backend/Applications/extensions.py
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache

jwt = JWTManager()
cors = CORS()
cache = Cache()
