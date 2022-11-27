from firebase_admin import credentials, initialize_app, auth, firestore
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.dbUtils import dbCollectionToSerializable, dbItemToSerializable

def createApp():
  app = Flask(__name__)
  return app



cred = credentials.Certificate('src/proyecto-integrado-65cf2-firebase-adminsdk-mkk3g-58bfa458f8.json')
defaultApp = initialize_app(cred)
# db = firestore.client()

app = createApp()
CORS(app)


# AUH USERS

@app.route('/api/firebase-admin/auth/users', methods=['GET'])
def getAuthUsers():
  dbData = auth.list_users().iterate_all()
  users = dbCollectionToSerializable(dbData, keepUID=True)

  response = jsonify(users)

  return response

@app.route('/api/firebase-admin/auth/user/<uid>', methods=['GET'])
def getAuthUser(uid):
  dbData = auth.get_user(uid)
  user = dbItemToSerializable(dbData, keepUID=True)

  response = jsonify(user)

  return response


# USERS

# @app.route('/api/firebase-admin/users', methods=['GET'])
# def getUsers():
#   dbData = db.collection('users').get()
#   users = dbCollectionToSerializable(dbData)

#   response = jsonify(users)

#   return response

# @app.route('/api/firebase-admin/user/<id>', methods=['GET'])
# def getUser(id):
#   dbData = db.collection('users').doc(id).get()
#   user = dbItemToSerializable(dbData)

#   response = jsonify(user)

#   return response


if __name__ == '__main__':
  app.run(debug = True, port = 9000)
