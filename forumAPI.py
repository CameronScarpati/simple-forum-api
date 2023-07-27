from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

users = {
    "user1": {"user": "Cameron James Scarpati"},
    "user2": {"user": "Charlie Ann Page"},
}
threads = {
    "thread1": {"thread": "Hello World!", "user": "Cameron James Scarpati"}
}

parser = reqparse.RequestParser()
parser.add_argument("user")
parser.add_argument("thread")

def abortIfUserIDDoesNotExist(userID):
    if userID not in users:
        abort(404, message="User: {} doesn't exist.".format(userID) + " Please post user.".format(userID))

def abortIfThreadIDDoesNotExist(threadID):
    if threadID not in threads:
        abort(404, message="Thread: {} doesn't exist.".format(threadID) + " Please post thread.".format(threadID))

# Allows you to get and delete a specific user using an ID.
class User(Resource):
    def get(self, userID):
        abortIfUserIDDoesNotExist(userID)
        return {userID: users[userID]} 
    
    def delete(self, userID):
        abortIfUserIDDoesNotExist(userID)
        del users[userID]
        return '', 204

# Allows you to get the list of all users and post them as well.
class UserList(Resource):
    def get(self):
        return users
    
    def post(self):
        args = parser.parse_args()
        userID = int(max(users.keys()).lstrip("user")) + 1
        userID = "user%i" % userID
        users[userID] = {"user": args["user"]}
        return users[userID], 201

# Allows you to get and delete a specific thread using an ID.
class Thread(Resource):
    def get(self, threadID):
        abortIfThreadIDDoesNotExist(threadID)
        return {threadID: threads[threadID]}
    
    def delete(self, threadID):
        abortIfThreadIDDoesNotExist(threadID)
        del threads[threadID]
        return '', 204
    
# Allows you to get the list of all threads (and who posted them) as well as post threads. If a user does not exist, that user is posted.
class ThreadList(Resource):
    def get(self):
        return threads
    
    def post(self):
        args = parser.parse_args()
        if users.get(args["user"]) == None:
            userID = int(max(users.keys()).lstrip("user")) + 1
            userID = "user%i" % userID
            users[userID] = {"user": args["user"]}
            threadID = int(max(threads.keys()).lstrip("thread")) + 1
            threadID ="thread%i" % threadID
            threads[threadID] = {"thread": args["thread"], "user": args["user"]}
            return threads[threadID], 201
        threadID = int(max(threads.keys()).lstrip("thread")) + 1
        threadID ="thread%i" % threadID
        threads[threadID] = {"thread": args["thread"], "user": args["user"]}
        return threads[threadID], 201
    
api.add_resource(UserList, "/users")
api.add_resource(User, "/User/<userID>")
api.add_resource(ThreadList, "/threads")
api.add_resource(Thread, "/Thread/<threadID>")

if __name__ == "__main__":
    app.run(debug=True)