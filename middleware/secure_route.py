from http import HTTPStatus
from flask import request, g 
from functools import wraps
from config.environment import SECRET
import jwt
from models.user import UserModel
from app import db

def secure_route(func):

  @wraps(func)
  def wrapper(*args, **kwargs):
    raw_token = request.headers.get('Authorization')
    print(raw_token)

    if not raw_token:
      return{"message": "this i Unauthorized"}, HTTPStatus.UNAUTHORIZED
    
    clean_token = raw_token.replace("Bearer ", "")

    try:
      payload = jwt.decode(
        clean_token,
        SECRET,
        "HS256"
      )

      user_id = payload["sub"]
      user = db.session.query(UserModel).get(user_id)
      if not user:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
      
      g.current_user = user
      print(user.username)

    except jwt.ExpiredSignatureError:
        return { "message": "maybe Unauthorized" }, HTTPStatus.UNAUTHORIZED
    except Exception:
        return { "message": "is it Unauthorized" }, HTTPStatus.UNAUTHORIZED

    return func(*args, **kwargs)

  return wrapper
