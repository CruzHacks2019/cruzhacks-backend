import cognitive_face as CF
"""

"""
SUB_KEY = '36fee94e28fa469fa8df5deec07c8f1c'
BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
PERSON_GROUP_ID = "people_two"
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUB_KEY)

response = CF.face.detect('tejas-test.jpg')
face_ids = [d['faceId'] for d in response]
print(face_ids)

identified_faces = CF.face.identify(face_ids, PERSON_GROUP_ID)
print(identified_faces)
