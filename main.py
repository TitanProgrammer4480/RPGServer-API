from flask import Flask, request, render_template, jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from classes.user import User
from classes.character import Character

import os

app = Flask(__name__)
cred = credentials.Certificate(os.getenv("firebase_cred"))

firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

def db_exists(collection, id):
  doc_ref = db.collection(collection).document(id)
  doc = doc_ref.get()
  if doc.exists:
    return True
  else:
    return False

@app.route("/", methods=["GET"])
def home():
  return render_template("home.html")

@app.route("/api/users", methods=["GET"])
def get_users():
  return_data = []
  docs = db.collection("users").stream()
  for i in docs:
    return_data.append(i.to_dict())
  return jsonify(return_data)


@app.route("/api/user", methods=["GET", "POST", "PUT", "DELETE"])
def manage_user():

  if request.method == "GET":
    data = request.get_json(force=True)
    if db_exists("users", data["uuid"]):
      doc_ref = db.collection("users").document(data["uuid"])
      doc = doc_ref.get()
      return doc.to_dict()
    else:
      return "false"

  elif request.method == "POST":
    data = request.get_json(force=True)
    if db_exists("users", data["uuid"]):
      return "false"
    else:
      user = User(username=data["username"], id=data["uuid"], char_slots=data["char_slots"], char_ids=data["char_ids"])
      db.collection("users").document(user.id).set(user.to_dict())
      return "true"
    
  elif request.method == "PUT":
    data = request.get_json(force=True)
    if db_exists("users", data["uuid"]):
      user = User(username=data["username"], id=data["uuid"], char_slots=data["char_slots"], char_ids=data["char_ids"])
      doc_ref = db.collection("users").document(data["uuid"])
      doc_ref.update(user.to_dict())
      return "true"
    else:
      return "false"
  
  elif request.method == "DELETE":
    data = request.get_json(force=True)
    if db_exists("users", data["uuid"]):
      db.collection("users").document(data["uuid"]).delete()
      return "true"
    else:
      return "false"
  

@app.route("/api/character", methods=["GET", "POST", "PUT", "DElETE"])
def manage_char():

  if request.method == "GET":
    data = request.get_json(force=True)
    if db_exists("chars", data["id"]):
      doc_ref = db.collection("chars").document(data["id"])
      doc = doc_ref.get()
      return doc.to_dict()
    else:
      return "false"

  elif request.method == "POST":
    data = request.get_json(force=True)
    if db_exists("chars", data["id"]):
      return "false"
    else:
      char = Character(id=data["id"], name=data["name"], location=data["location"], race=data["race"], specialisation=data["specialisation"], skills=data["stats"]["skills"], abilities=data["stats"]["abilities"], quests=data["stats"]["quests"])
      db.collection("chars").document(char.id).set(char.to_dict())
      return "true"
  
  elif request.method == "PUT":
    data = request.get_json(force=True)
    if db_exists("chars", data["id"]):
      char = Character(id=data["id"], name=data["name"], location=data["location"], race=data["race"], specialisation=data["specialisation"], skills=data["stats"]["skills"], abilities=data["stats"]["abilities"], quests=data["stats"]["quests"])
      db.collection("chars").document(char.id).set(char.to_dict())
      return "true"
    else:
      return "false"
  
  elif request.method == "DELETE":
    data = request.get_json(force=True)
    if db_exists("chars", data["id"]):
      db.collection("chars").document(data["id"]).delete()
      return "true"
    else:
      return "false"
