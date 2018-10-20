from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# users = [
#     {
#         "name" : "Nicolas",
#         "age": 42,
#         "occupation": "Network Eng"
#     },
#     {
#         'name' : 'Evan',
#         'age': 29,
#         "occupation": "CS Eng"
#     },
#     {
#         "name" : "Jess",
#         "age": 35,
#         "occupation": "Bikar"
#     }
#     ]

class DB(Resource):
    def get(self, name):
        # for user in users:
        #     if(name == user["name"]):
        #         return user, 200
        # return "user not found", 404
        return "this is a test get request", 200

    def post(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument("age")
        # parser.add_argument("occupation")
        # args = parser.parse_args()

        # for user in users:
        #     if(name == user["name"]):
        #         return "User with name {} already exists".format(name), 400

        # user = {
        #     "name": name,
        #     "age": args["age"],
        #     "occupation": args["occupation"]
        # }
        # users.append(user)
        # return user, 201
        return "this is a test post request", 201

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument("age")
        # parser.add_argument("occupation")
        # args = parser.parse_args()

        # for user in users:
        #     if(name == user["name"]):
        #         user["age"] = args["age"]
        #         user["occupation"] = args["occupation"]
        #         return user, 200

        # user = {
        #     "name": name,
        #     "age": args["age"],
        #     "occupation": args["occupation"]
        # }
        # users.append(user)
        # return user, 201
        return "this is a test put request", 200

    def delete(self, name):
        # global users
        # users = [user for user in users if user["name"] != name]
        # return "{} is deleted".format(name), 200
        return "this is a test delete request", 200

api.add_resource(User, "/DB/<string:name>")
app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)
