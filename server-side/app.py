from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
import json, urllib, requests
import random

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

        # user = 
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

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    # apiurl = "https://launchlibrary.net/1.3/launch"
    # res = requests.get(apiurl)
    jsonFile = open('app.json')
    jsonText = jsonFile.read()
    json_data = json.loads(jsonText)
    # json_data = res.json()

    return render_template('home.html', launches=json_data)

# @app.route('/about')
# def about():
#     return render_template('about.html')


@app.route('/get', methods=['GET'])
def getDB():
    # pollutionJson = getFromDB('pollutionInfo')
    # return pollutionJson
    return 'Success GET', 999

@app.route('/launch/<launchID>')
def launch(launchID):
    # img =

    jsonFile = open('app.json')
    jsonText = jsonFile.read()
    json_data = json.loads(jsonText)
    # json_data = res.json()
    for launch in json_data:
        if (launch['launchid']) == launchID:
            return render_template('launch.html', launch=launch, weather=str(random.randint(72,105)))
   
    # return render_template('launch.html', launch)



# @app.route('/launch') 
# def launch():
#     return render_template('launch.html')

# @app.route('/launch2')
# def launch_2():
#     return render_template('launch1.html')

# @app.route('/launch3')
# def launch_3():
#     return render_template('launch2.html')

if __name__ == '__main__':
	app.run(debug=True)