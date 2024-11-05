from flask import Flask, request, render_template, jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from classes.user import User
from classes.character import Character

app = Flask(__name__)

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "mc-server-438309",
  "private_key_id": "a172d08c5d85015f9859b1edb7216f9e080fad8e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCZTIePmAQxHVJY\nDC8wy6xO/VRyy2PFw6oFU7v+o9HdY/Vz5qWsxJOMWlSSSFlzY9JhQGiZXJL8kRQx\nkrJARFCebqcZh+noMbrbsc3GQDl0Eu31DUIU0r3bH61F/W3Hp+2wsZ9udY8El017\nL59oi7B2BvdyrJ3vSHHR3u+NbzWqyQ7AW79+BqIlTN2UAU3U2PTEIxdB5NUMBxIA\n6vCYl670yAYFmAn14ZpcNA+zeHMGkSPb4f9kmN5xTDVu9GxnZ+iYGo2vd3RrH4l4\nW3Vw23YIxJT5YXvkkxYQxvTA5NrHR84oc7GYikPbDtfTyxBLa4yqgQoP9bCgFyFG\n+u15Z/WdAgMBAAECggEABWN/k9O/3Wauvy2VUxRaUoR+4gRs1bOuMyyYV27ZDEXK\nY0u7/EwpPeTrjLMdyvu7BAZtAkcTEn916EJ6/G/qUiLSL79HCekFmn5CZlZ+d6pa\nrdo6UCUSlI/cNWgxvbPMCbiUr42cDtIdBSGERvsWo295irWKpo0zXnqpsZ0O3Qdj\ndXN4HC52pqrD4XkJXcjsVuQLDKfNP5Lr9TtGRwrLsk71Y5b11a3/qwsz4A0VOFv5\nez56/14FsQA8fnkJy2S3SuKpfBq4c0i+GzH1l4NneumnSrQwJhO0qTEIWBNO4+1b\ntPWr6efizWQXLo2897hZpRtfCqK0ajaORDHHv71meQKBgQDRkrS5cRUZN/g0Vz8u\nOFV59YGApQ7FwguyTrSmrYBQ6Ey8nbM6cZ4jlf+UgKt/kxFXwjaMgvrc99in4YpV\nBFBxjDURpTZS/hScCnoLKEkYxtb4ZTooDmCXlVyhGpPLVZJXdIeTyN47AiOoKwwH\noaHpk9C51syEbQCEaMYawJ+guwKBgQC7Qmi3KLFW07W5Ll5uOnAA0AyXpXDqPh7L\nmOW66bvYat1tghSYQ5t73Yoq4/RGYW1+x9qylrNyQ3wF1nWmf+1qU8iNCU+UI1hu\n8bsZytuxCs+uMSbJykaCgoeWnT44dHGHFQ0SNLkBTsVGy/tRFOSBLS6I5W6/Qjhv\ny4AbzNDphwKBgQCp5e9RbxWVrkQv2pND2zOgfaGRMz64n8lvslLN1VZzQQAE4SwN\ns1Jqsw3RzEY8VHP421/xpbXOMbeY0kWdCrRUeUAEoBVcTtNSdUPfi7dGuNxJ33a4\nRn+UI+hGSw+KBkNvVu8apftThzZ0/QDxpt1mSQkrv7FpohyLO41u3r4KRQKBgE6/\nVpnvmuQQk9MUFNH18TPmSeVbxWg8R2cHHVTFBiG0jvmGQnLlu3UTbQ8sXYVbY1h1\nYxrHFR9wEa/CyCcElSqpoSTuTXDWjFHbhfsKu+hvy3ZNZSpmzdAEZFCKP6guD6/m\nwmBtm39ZSMzE6yLlzlIkVfVrxm7XwjQBOBZ4w0HxAoGAGhsB9tT8W4TyQX0mh4IV\njQjR2OUhcqgx85SsjOdxuEB4EHvXIKjEbj1WdK2lcdMEcF7e2j2slXcymLGjVQyj\nJsHoRDN2ultIAFDNSD+mNnZIg4J1844PGMs43+ilXtkzHU6UStxVQsWOP9K0hZ4x\n78b7fitxWuuRyvsscw2RxTo=\n-----END PRIVATE KEY-----\n",
  "client_email": "admin-674@mc-server-438309.iam.gserviceaccount.com",
  "client_id": "114209518131795175132",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admin-674%40mc-server-438309.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

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
