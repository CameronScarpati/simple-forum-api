from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from forumDatabase import *

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("title")
parser.add_argument("user_id")
parser.add_argument("message")

forum_db.connect()
forum_db.create_tables([UserDB, PostDB, ThreadDB])

threads = [{"id" : 1, "title" : "New Project Idea", "user_id" : 1, "posts": [1, 2]}]

class Users(Resource):
    def get(self):
        users = []
        for user in UserDB.select():
            users.append({"id" : user.id, "name" : user.name})

        return users

    def post(self):
        args = parser.parse_args()
        id = UserDB.select().count() + 1

        try:
            UserDB.create(id = int(id), name = args["name"])
        except BaseException:
            abort(500, message="The username {} has already been taken.".format(args["name"]) + " Please try another.".format(args["name"]))

        return int(id), 201
    
class User(Resource):
    def get(self, id: int):
        if int(id) > UserDB.select().count():
            abort(404, message="This user id does not exist. Please input a valid user id.")

        foundUser = UserDB.select().where(UserDB.id == int(id))
        return {"id" : int(id), "name" : foundUser.name}, 200

class Threads(Resource):
    def get(self):
        threads = []
        for thread in ThreadDB.select():
            threads.append({"id" : thread.id, "title" : thread.title, "user_id" : thread.user_id.id})

        return threads
    
    def post(self):
        args = parser.parse_args()

        id = ThreadDB.select().count() + 1

        if int(args["user_id"]) > UserDB.select().count():
            abort(500, message="This user id does not exist. Please input a valid user id.")

        ThreadDB.create(id = int(id), title = args["title"], user_id = args["user_id"])

        return int(id), 201
    
class Thread(Resource):
    def get(self, id: int):
        if int(id) > ThreadDB.select().count():
            abort(404, message="This thread id does not exist. Please input a valid thread id.")

        foundThread = ThreadDB.select().where(ThreadDB.id == int(id))
        return {"id" : int(id), "title" : foundThread.title, "user_id" : foundThread.user_id.id}, 200
    
class Posts(Resource):
    def get(self, thread_id: int):
        if int(thread_id) > ThreadDB.select().count():
            abort(404, message="This thread id does not exist. Please input a valid thread id.")

        posts = []
        for post in PostDB.select().where(PostDB.thread_id == thread_id):
            posts.append({"id" : post.id, "message" : post.message, "user_id" : post.user_id.id})

        return posts
    
    def post(self, thread_id: int):
        args = parser.parse_args()

        id = PostDB.select().count() + 1

        if int(thread_id) > ThreadDB.select().count():
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        if int(args["user_id"]) > UserDB.select().count():
            abort(500, message="This user id does not exist. Please input a valid user id.")

        PostDB.create(id = int(id), message = args["message"], user_id = args["user_id"], thread_id = int(thread_id))

        return int(id), 201

class Post(Resource):
    def get(self, thread_id: int, post_id: int):
        if int(thread_id) > ThreadDB.select().count():
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        if int(post_id) > PostDB.select().count():
            abort(404, message="This post id does not exist. Please input a valid post id.")
        if PostDB.select().where(PostDB.id == int(post_id)).get().thread_id != int(thread_id):
            abort(500, message="This post id is not contained within this thread. Please input a valid post id for this thread or a valid thread id for this post.")

        foundPost = PostDB.select().where(PostDB.id == int(post_id)).get()
        return {"id" : int(post_id), "message" : foundPost.message, "user_id" : foundPost.user_id.id}, 200

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<id>")
api.add_resource(Threads, "/threads")
api.add_resource(Thread, "/threads/<id>")
api.add_resource(Posts, "/threads/<thread_id>/posts")
api.add_resource(Post, "/threads/<thread_id>/posts/<post_id>")

if __name__ == "__main__":
    app.run(debug=True)