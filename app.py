from flask import Flask, Response, request
import json
import pymongo
import dns
from bson.objectid import ObjectId
import env

app = Flask(__name__)

try:
    cleint = pymongo.MongoClient(env.MONGO_URI,serverSelectionTimeoutMS=5000)
    db = cleint["flask-mongo"]
except Exception:
    print("Unable to connect to the server.")

############################################

@app.route("/users", methods=["GET"])
def getAllUser():
    try:
        data = list(db.people.find())
        print(data)
        
        for people in data:
            people["_id"] = str(people["_id"])

        callback = {
            "message" : "success read user",
            "data" : data
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )
    except Exception as e:
        print(e)
        callback = {
            "message" : "cannot read user",
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )
@app.route("/users/<user_id>", methods=["GET"])
def getUserById(user_id):
    try:
        user_id = ObjectId(user_id)
        print(user_id)
        data = db.people.find_one({"_id": user_id})

        if(data is None):
            callback = {
                "message" : "user not found"
            }
        else:
            data["_id"] = str(data["_id"])

            callback = {
                "message" : "success read user",
                "data" : data
            }
        return Response(
            response = json.dumps(callback),
            status = 200,
            mimetype= "application/json"
        )
    except Exception as e:
        print(e)
        callback = {
            "message" : "cannot read user",
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )
@app.route("/users/<user_id>", methods=["PUT"])
def updategUserById(user_id):
    try:
        user_id = ObjectId(user_id)
        print(user_id)
        find = {"_id" : user_id}
        setValue = {
            "$set" : {
                "name" : request.form['name'],
                "age" : request.form["age"]
            }
        }
        resp = db.people.update_one(find,setValue)
        print(resp.upserted_id)

        if(resp.modified_count <= 0):
            callback = {
                "message" : f"none data updated"
            }
        else:
            callback = {
                "message" : f"success update {resp.modified_count} user",
                "data" : {
                    "_id" : str(user_id)
                }
            }
        return Response(
            response = json.dumps(callback),
            status = 200,
            mimetype= "application/json"
        )
    except Exception as e:
        print(e)
        callback = {
            "message" : "cannot update user",
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )

@app.route("/users/<user_id>", methods=["DELETE"])
def deleteUserById(user_id):
    try:
        user_id = ObjectId(user_id)
        print(user_id)
        data = db.people.delete_one({"_id": user_id})

        if(data.deleted_count <= 0):
            callback = {
                "message" : f"none data deleted",
            }    
        else:
            callback = {
                "message" : f"success delete {data.deleted_count} user",
                "data" : {
                    "_id" : str(user_id)
                }
            }
        
        return Response(
            response = json.dumps(callback),
            status = 200,
            mimetype= "application/json"
        )
    except Exception as e:
        print(e)
        callback = {
            "message" : "cannot delete user",
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = {
            "name" : request.form['name'],
            "age" : request.form["age"]
        }
        resp = db.people.insert_one(data)
        callback = {
            "message" : "user created",
            "data" : {
                "_id" : str(resp.inserted_id)
            }
        }
        print(callback)
        return Response(
            response = json.dumps(callback),
            status = 201,
            mimetype= "application/json"
        )
    except Exception as e:
        print(e)
        callback = {
            "message" : "cannot create users",
        }
        return Response(
            response = json.dumps(callback),
            status = 500,
            mimetype= "application/json"
        )
    

############################################

if __name__ == "__main__":
    app.run(port=5000, debug=True)