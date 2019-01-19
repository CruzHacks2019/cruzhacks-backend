import cognitive_face as CF
from APIKey import *
import glob
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('project-anti-alz-firebase-adminsdk-zlh54-decaa0ce0a.json')
default_app = firebase_admin.initialize_app(cred)
"""
2019 Cruzhacks
"""
class APIClient:

    def __init__(self, db_id):
        self.BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
        self.PERSON_GROUP_ID = db_id
        CF.BaseUrl.set(self.BASE_URL)
        CF.Key.set(SUB_KEY)

    def create_database(self, name):
        CF.person_group.create(self.PERSON_GROUP_ID, name)

    def add_person(self, name, user_data, img_dir):
        response = CF.person.create(self.PERSON_GROUP_ID, name, user_data)
        person_id = response["personId"]
        firebase_admin.db.push(response)
        for img in glob.glob(img_dir):
            CF.person.add_face(img, self.PERSON_GROUP_ID, person_id)

    def return_message_from_face(self, path_to_img):
        response = CF.face.detect(path_to_img)
        face_ids = [d['faceId'] for d in response]
        identified_faces = CF.face.identify(face_ids, self.PERSON_GROUP_ID)
        person_id = identified_faces[0]['candidates'][0]['personId']
        response = CF.person.get(self.PERSON_GROUP_ID, person_id)
        return response 

    def print_status(self):
        response = CF.person_group.get_status(self.PERSON_GROUP_ID)
        status = response['status']
        print(status)   

    def print_list(self):
        print(CF.person.lists(self.PERSON_GROUP_ID))

    def train_data(self):
        CF.person_group.train(self.PERSON_GROUP_ID)


