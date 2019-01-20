from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
import base64
from hashlib import md5
from APIClient import *
import firebase_admin
from firebase_admin import credentials, db
import time

cred = credentials.Certificate('project-anti-alz-firebase-adminsdk-zlh54-decaa0ce0a.json') 
# firebase_admin.initialize_app(cred, {'databaseURL' : 'https://project-anti-alz.firebaseio.com/'})
root = db.reference()

# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = 'history-images-3519435695'
# bucket = storage_client.create_bucket(bucket_name)
"""

"""
app = Flask(__name__)
bootstrap = Bootstrap(app)
client = APIClient("people_six")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/detect-face', methods=['POST'])
def detect_face():
    img_content = request.data
    decoded_img = base64.b64decode(img_content)
    img_path = "uploads/" + md5(img_content.decode().encode('utf-8')).hexdigest() + ".png"
    with open(img_path, "wb") as fh:
        fh.write(decoded_img)

    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    destination_blob_name = md5(img_content.decode().encode('utf-8')).hexdigest()
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename("uploads/" + destination_blob_name + ".png")
    print('File {} uploaded to {}.'.format("uploads/" + destination_blob_name + ".png", destination_blob_name))

    url = "https://storage.cloud.google.com/history-images-3519435695/"+ destination_blob_name

    result = client.return_message_from_face(img_path)
    # this is a list now, what happens if the list is empty?
    print(result)
    if len(result) > 0:
        result[0]['msg'] = "You met " + result[0]["name"] + " he is your " + result[0]["userData"] + "."
    else:
        print("Empty List")
        return(jsonify({"error":"You we're not found."}))


    user_ref = root.child('history')
    user_ref.child(result[0]['personId']).set(
        {
            'imgUrls': url,
            'time': int(time.time() * 1000)
        }
    )

    return jsonify(result)

@app.route('/reminders', methods=['GET'])
def get_reminders():
    return jsonify(client.fetch_all_reminders())

@app.route("/update_azure_db", methods=['POST'])
def update_azure_db():
    img_content = request.data
    decoded_img = base64.b64decode(img_content)
    img_path = "uploads/" + md5(img_content.decode().encode('utf-8')).hexdigest() + ".png"
    client.add_person("Need to FIll Name", "Relationship", img_path)
    return jsonify({"error":"Do not access"})


if __name__=='__main__':
    app.run(debug=True)
