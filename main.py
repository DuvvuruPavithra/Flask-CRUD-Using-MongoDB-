import pymongo
from flask import Flask, Response, json, request, render_template
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    db = mongo.contacts
    mongo.server_info()  # trigger exception if cannot connect to db
except:
    print("ERROR - CANNOT connect to db ")


@app.route("/users", methods=["GET"])
def all_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        print(data)
        return Response(response=json.dumps(data), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Cannot read users "}),
            status=500,
            mimetype="application/json")


@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"firstname": request.form["firstname"],
                "lastname": request.form["lastname"],
                "address": request.form["address"],
                "state": request.form["state"],
                "city": request.form["city"],
                "mobileNumber": request.form["mobileNumber"]
                }
        dbResponse = db.users.insert_one(user)
        return render_template("home.html")

        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps({"message": "user created", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json")
    except Exception as ex:
        print(ex)


@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"lastname": request.form["lastname"]}}

        )
        if dbResponse.modified_count == 1:
            return Response(response=json.dumps({"message": "user updated successfully"}), status=200,
                            mimetype="application/json")

        return Response(response=json.dumps({"message": "nothing to update"}), status=200,
                        mimetype="application/json")

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "sorry cannot update user"}), status=500, mimetype="application/json")


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response=json.dumps({"message": "user deleted", "id": f"{id}"}), status=200,
                mimetype="application/json")

        return Response(
            response=json.dumps({"message": "user not found", "id": f"{id}"}), status=200, mimetype="application/json")

    except Exception as ex:
        print("*******************")
        print(ex)
        print("*******************")
        return Response(
            response=json.dumps({"message": "sorry cannot delete user"}), status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run(debug=True, port=801)
