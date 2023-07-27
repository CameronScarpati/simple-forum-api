from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    #app.run(debug=True)



    users = {
        "user1": {"user": "Cameron James Scarpati"},
        "user2": {"user": "Charlie Ann Page"},
    }
    threads = {
        "thread1": {"thread": "Hello World!", "user": "Cameron James Scarpati"},
        "thread2": {"thread": "Goodbye World!", "user": "Charlie Ann Page"}
    }

    user = "Cameron James Scarpati"

    print(threads.values())
