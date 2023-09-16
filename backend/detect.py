import face_recognition, base64, io
import db
import numpy as np
from PIL import Image


def get_face_encoding(image_array: np.ndarray):
    try:
        encodings = face_recognition.face_encodings(image_array)
        if len(encodings) > 1:
            raise ValueError("More than one face detected, only keep one")
        return encodings[0]
    except IndexError:
        raise IndexError("No face detected!")


async def check_face_in_db(image_array) -> int | np.ndarray:
    faces = await db.get_all_faces()
    unknown_encoding = get_face_encoding(image_array)
    for face in faces:
        unknown_encoding = np.array(unknown_encoding)
        encoding = np.array(face.encoding)

        results = face_recognition.compare_faces([encoding], unknown_encoding)
        if results[0]:
            return face.user.id
    return unknown_encoding


def decode_image_to_array(decoded_image: str):
    image_data_binary = base64.b64decode(decoded_image)
    img_arr = np.array(Image.open(io.BytesIO(image_data_binary)).convert("RGB"))
    return img_arr
