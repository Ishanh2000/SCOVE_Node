# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
# ssh -i "698.pem" ubuntu@ec2-18-222-200-30.us-east-2.compute.amazonaws.com
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
import json

IMG_PATH = "./img/"

app = Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/scove")
db = mongodb_client.db

@app.route("/add_one")
def add_one():
  db.todos.insert_one({'title': "todo title", 'body': "todo body"})
  return jsonify(message="success")

@app.route("/events", methods=["GET", "POST", "DELETE"])
def events():
  if request.method == "GET":
    return "GETTER"

  if request.method == "POST":
    try:
      data = None
      for f in request.files:
        if f != "json": request.files[f].save(IMG_PATH + f)
        else: data = json.loads(request.files["json"].read()) # 'start', 'phase', 'isMischief', 'images'
      

      x = db.events.find_one({ "start" : data["start"] })
      if x == None:
        db.events.insert_one({
          "start" : data["start"],
          f"phase_{data['phase']}" : { "isMischief" : data["isMischief"], "images" : data["images"] }
        })
      else:
        db.events.update_one( { "_id" : x["_id"] }, { "$set" : {
          f"phase_{data['phase']}" : { "isMischief" : data["isMischief"], "images" : data["images"] }
        } }, upsert=False)

      # if phase 2 - take optimistic attendance if not isMischief
      if (data["phase"] == 2) and not data["isMischief"]:
        db.opt_att.insert_one({
          "start" : data["start"],
          "attTime" : data["images"][-1]["time"],
          "faceLabel" : data["images"][-1]["status"]["faceLabel"],
        })

      # if phase 3 - delete optimistic attendance if isMischief
      if (data["phase"] == 3) and data["isMischief"]:
        db.opt_att.remove({ "start" : data["start"] })
        
      return "SUCCESS"

    except:
      return "ERROR"

  if request.method == "DELETE":
    return "DELETER"


@app.route("/attendance", methods=["GET", "POST", "DELETE"])
def attendance():
  if request.method == "GET":
    return "GETTER"

  if request.method == "POST":
    try:
      data = request.json # 'start', 'attTime', 'faceLabel', 'avgTemp', 'maskLabel', 'disallowReason'
      
      # delete optimistic attendance
      db.opt_att.remove({ "start" : data["start"] })

      # take real attendance
      db.att.insert_one(data)

      return "SUCCESS"

    except:
      return "ERROR"

  if request.method == "DELETE":
    return "DELETER"


@app.route("/")
def hello_world():
  return "Hello, World!"
