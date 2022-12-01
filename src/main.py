from firebase_admin import credentials, initialize_app, auth, firestore
from flask import Flask, jsonify, request, make_response, Response, abort
from flask_cors import CORS, cross_origin
import sys
import json

from utils.dbUtils import dbCollectionToSerializable, dbItemToSerializable

def createApp():
  app = Flask(__name__)
  return app



cred = credentials.Certificate('src/proyecto-integrado-65cf2-firebase-adminsdk-mkk3g-58bfa458f8.json')
defaultApp = initialize_app(cred)
# db = firestore.client()

app = createApp()
CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}})

# app.config['CORS_HEADERS'] = 'Content-Type'

# https://stackoverflow.com/questions/39550920/flask-cors-not-working-for-post-but-working-for-get/57735363#57735363


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


@app.route('/api/firebase-admin/auth/user/add', methods=['POST'])
def addAuthUser():
  authUser = request.json

  try:
    dbData = auth.create_user(email=authUser['email'], password=authUser['password'])
  except Exception as error:
    return Response(f'"{error}"', status=502, mimetype='application/json')

  newAuthUser = dbItemToSerializable(dbData, keepUID=True)

  return Response(json.dumps(newAuthUser), mimetype='application/json')

@app.route('/api/firebase-admin/auth/user/delete', methods=['POST'])
def deleteAuthUser():
  if request.method != 'POST':
    abort()

  authUserUID = request.json

  try:
    auth.delete_user(authUserUID)
  except Exception as error:
    return Response(f'"{error}"', status=502, mimetype='application/json')

  return Response(f'{{"authUserDeletedUID": "{authUserUID}"}}', mimetype='application/json')


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
