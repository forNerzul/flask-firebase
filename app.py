from flask import Flask, render_template, request
import firebase_admin # Firebase SDK
from firebase_admin import credentials, firestore # Firebase SDK


# use a service account
cred = credentials.Certificate('test-project-8c58b-firebase-adminsdk-n8t2e-7b78c29e99.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# crear una conexion con firebase emulator
# cred = credentials.Certificate('test-project-8c58b-firebase-adminsdk-n8t2e-7b78c29e99.json')
# firebase_admin.initialize_app({ 'projectId': 'test-project-8c58b', 'databaseURL': 'http://localhost:8080' })
# db = firestore.client()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/insert', methods=['POST'])
def insert():
    # Get data from request
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Print data to console

    print("""
        username: {}
        password: {}
          """.format(username, password)
          )

    # Insert data into database
    
    doc_ref = db.collection('users').document(username)
    doc_ref.set({
        'password': password
    })

    response = {
        'status': 200,
        'message': 'success',
    }
    return response

@app.route('/api/login', methods=['POST'])
def login():
    # Get data from request
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Get users from database
    users_ref = db.collection('users')
    docs = users_ref.stream()
    for doc in docs:
        if doc.id == username:
            if doc.to_dict()['password'] == password:
                response = {
                    'status': 200,
                    'message': 'success',
                }
                return response
            else:
                response = {
                    'status': 400,
                    'message': 'password incorrect',
                }
                return response