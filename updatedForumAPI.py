from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("title")
parser.add_argument("user_id")
parser.add_argument("message")
parser.add_argument("user")

users = [{"id" : 1, "name" : "Cameron James Scarpati"}, {"id": 2, "name" : "Charlie Ann Page"}]
threads = [{"id" : 1, "title" : "New Project Idea", "user_id" : 1, "posts": [1, 2]}]
posts = [{"id" : 1, "message" : "I could create something that interacts with all of my smart lighting and can be used to match the game I am currently playing.", "user_id" : 1}, 
         {"id" : 2, "message" : "I could create an in-game overlay for all of my steamgames that helps me more easily track achievements and status as well as easily link guides to solving them if I am stumped.", "user_id" : 2}]

class Users(Resource):
    def get(self):
        return users

    def post(self):
        args = parser.parse_args()

        for n in users:
            if args["name"] == n["name"]:
                abort(500, message="The username {} has already been taken.".format(args["name"]) + " Please try another.".format(args["name"]))

        id = len(users) + 1
        users.append({"id" : id,"name" : args["name"]})
        return int(id), 201
    
class User(Resource):
    def get(self, id: int):
        if int(id) > len(users):
            abort(404, message="This user id does not exist. Please input a valid user id.")
        return users[int(id) - 1], 200

class Threads(Resource):
    def get(self):
        return threads
    
    def post(self):
        args = parser.parse_args()

        id = len(threads) + 1

        if int(args["user_id"]) > len(users):
            abort(500, message="This user id does not exist. Please input a valid user id.")

        threads.append({"id" : id, "title" : args["title"], "user_id" : args["user_id"], "posts": []})
        return int(id), 201
    
class Thread(Resource):
    def get(self, id: int):
        if int(id) > len(threads):
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        return threads[int(id) - 1], 200
    
class Posts(Resource):
    def get(self, thread_id: int):
        if int(thread_id) > len(threads):
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        return posts
    
    def post(self, thread_id: int):
        args = parser.parse_args()

        id = len(posts) + 1

        if int(thread_id) > len(threads):
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        if int(args["user_id"]) > len(users):
            abort(500, message="This user id does not exist. Please input a valid user id.")

        threads[int(thread_id) - 1]["posts"].append(int(id))
        posts.append({"id" : int(id), "message" : args["message"], "user_id" : args["user_id"]})
        return int(id), 201

class Post(Resource):
    def get(self, thread_id: int, post_id: int):
        if int(thread_id) > len(threads):
            abort(404, message="This thread id does not exist. Please input a valid thread id.")
        if int(post_id) > len(posts):
            abort(404, message="This post id does not exist. Please input a valid post id.")
        if int(post_id) not in threads[int(thread_id) - 1].get("posts"):
            abort(500, message="This post id is not contained within this thread. Please input a valid post id for this thread or a valid thread id for this post.")
        return posts[int(post_id) - 1], 200

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<id>")
api.add_resource(Threads, "/threads")
api.add_resource(Thread, "/threads/<id>")
api.add_resource(Posts, "/threads/<thread_id>/posts")
api.add_resource(Post, "/threads/<thread_id>/posts/<post_id>")

if __name__ == "__main__":
    app.run(debug=True)