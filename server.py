# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
# ssh -i "698.pem" ubuntu@ec2-18-222-200-30.us-east-2.compute.amazonaws.com
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
import json
from bson import json_util
from infer import face_labels
from time import time

IMG_PATH = "./img/"
DAY = 86400 # length of a day in seconds

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
    args = dict(request.args)
    _from, _to, _expand, _person = args.get("from"), args.get("to"), args.get("expand"), args.get("person")

    try:
      if _from: _from = float(_from)
      if _to: _to = float(_to)
      if _expand not in [ None, "0", "1" ]: raise Exception()
      _expand = (_expand == "1")
    except:
      return "Expected format: { from (float), to (float), expand (0/1), person (string) }", 400
    
    if _from is None and _to is None: _to = time(); _from = _to - (2*DAY)
    elif _from is None: _from = _to - (2*DAY)
    elif _to is None: _to = _from + (2*DAY)

    if ((_to-_from) > (2*DAY)) and not _expand:
      return "Query interval larger than 48 hrs. Set \"expand=1\" for larger intervals.", 400
    
    qry = { "attTime" : { "$gte" : _from, "$lte" : _to } } # query
    if _person: qry["faceLabel"] = _person
    q = db.att.find(qry)

    return {
      "att" : json.loads(json.dumps(list(q), default=json_util.default)), # TODO: kindly simplify this - code should not be very complicated
      "all" : face_labels
    }

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
