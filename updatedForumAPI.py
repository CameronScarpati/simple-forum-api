from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name")

users = [{"id": 1, "name" : "Cameron James Scarpati"}, {"id": 2, "name" : "Charlie Ann Page"}]

class Users(Resource):
    def get(self):
        return users

    def post(self):
        args = parser.parse_args()

        print(args["name"])

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

api.add_resource(Users, "/users")
api.add_resource(User, "/users/<id>")

if __name__ == "__main__":
    app.run(debug=True)