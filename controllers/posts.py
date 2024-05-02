from http import HTTPStatus



from flask import Blueprint, request, g 
from marshmallow.exceptions import ValidationError
from middleware.secure_route import secure_route
from models.post import PostModel
# from models.user import UserModel
from serializers.post import PostSchema
from serializers.user import UserSchema
from app import db

post_schema = PostSchema()
user_schema = UserSchema()

router = Blueprint("posts", __name__)

#  ------------------------ GET ALL POSTS --------------------------
@router.route("/posts", methods=["GET"])
def get_posts():

    posts = PostModel.query.all()

    return post_schema.jsonify(posts, many=True)


#  ------------------------ GET A SINGLE POST --------------------------
@router.route("/posts/<int:post_id>", methods=["GET"])
def get_single_post(post_id):
    post = PostModel.query.get(post_id)

    if not post:
        return {"message": "No post found"}, HTTPStatus.NOT_FOUND
  
    return post_schema.jsonify(post)


#  ------------------------ POST A POST --------------------------
@router.route("/posts", methods=["POST"])
@secure_route
def create():
    post_dictionary = request.json

    try:
        post = post_schema.load(post_dictionary)
        post.user_id = g.current_user.id
        print(post_dictionary)
        post.save()
    
        return post_schema.jsonify(post)
  
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong!"}, HTTPStatus.UNPROCESSABLE_ENTITY
    except Exception as e: 
        print(e)
        return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR


    #  ------------------------ DELETE A POST --------------------------
@router.route("/posts/<int:post_id>", methods=["DELETE"])
@secure_route
def remove(post_id):
    post_to_delete = db.session.query(PostModel).get(post_id)

    if not post_to_delete:
        return {'message':'Post not found'}, HTTPStatus.NOT_FOUND
    
    if post_to_delete.user_id != g.current_user.id:
        return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
  
    post_to_delete.remove()
    return "", HTTPStatus.NO_CONTENT

  #  ------------------------ UPDATE A POST --------------------------
@router.route("/posts/<int:post_id>", methods=["PUT", "PATCH"])
@secure_route
def update_post(post_id):
    post_dictionary = request.json

    existing_post = PostModel.query.get(post_id)

    if not existing_post:
        return {"message": "No post found"}, HTTPStatus.NOT_FOUND
   
    try:
        if existing_post.user_id != g.current_user.id:
            return { "message": "This is not your post! Maybe try another" }, HTTPStatus.UNAUTHORIZED

        post = post_schema.load(
           post_dictionary,
           instance=existing_post, 
           partial=True
        )

        post.save()
    except ValidationError as e:
        return {"errors": e.messages, "message": "Something went wrong"}
    return post_schema.jsonify(post), HTTPStatus.OK
