from dotenv import load_dotenv
load_dotenv()

import face_recognition, os, cv2
import db
import numpy as np


def get_face_encoding():
    vid = cv2.VideoCapture(os.getenv("VIDEO_URL"))
    _, frame = vid.read()
    image_array = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # image_array = np.array(image_array).astype("uint8")
    print(image_array)
    try:
        encodings = face_recognition.face_encodings(image_array)
        # print(enc)
        if len(encodings) > 1:
            raise ValueError("More than one face detected, only keep one")
        return encodings[0]
    except IndexError:
        raise IndexError("No face detected!")


async def check_face_in_db() -> str | None:
    faces = await db.get_all_faces()
    unknown_encoding = get_face_encoding()
    for face in faces:
        unknown_encoding = np.array(unknown_encoding)
        encoding = np.array(face.encoding)

        results = face_recognition.compare_faces([encoding], unknown_encoding)
        if results[0]:
            return face.user.name
