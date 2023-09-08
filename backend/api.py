from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from db import get_all_faces, add_face
from detect import get_face_encoding, check_face_in_db, decode_image_to_array
from pydantic import BaseModel

app = FastAPI()
prisma = Prisma(auto_register=True)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


# TODO: Send the grayscale image only
class AddFaceBody(BaseModel):
    name: str
    image_encoding: str


class GetEncodingBody(BaseModel):
    image_encoding: str


class ImageData(BaseModel):
    image_encoding: str


class CheckFaceBody(BaseModel):
    image_encoding: str


@app.on_event("startup")
async def startup():
    print("startup")
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    print("shutdown")
    await prisma.disconnect()


@app.get("/all-faces")
async def get_faces():
    return {k: v for k, v in enumerate(await get_all_faces())}


@app.post("/add-face")
async def _add_face(body: AddFaceBody):
    error = ""
    try:
        image_encoding = decode_image_to_array(body.image_encoding)
        face = await add_face(body.name, image_encoding)
        return face
    except IndexError:
        error = "No faces found, show face and try again"

    except ValueError:
        error = "More than one face found, remove additional faces"

    return {"error": error}


@app.get("/face-encoding")
async def _get_face_enconding(image: ImageData):
    error = ""
    try:
        image_array = decode_image_to_array(image.image_encoding)
        enc = get_face_encoding(image_array)
        print(enc)
        return {"success": True}
    except IndexError:
        error = "No faces found, show face and try again"

    except ValueError:
        error = "More than one face found, remove additional faces"
    print(error)
    return {"error": error}


@app.get("/check-face")
async def _check_face(image: ImageData):
    error = ""
    try:
        image_array = decode_image_to_array(image.image_encoding)
        name = await check_face_in_db(image_array)
        print({"name": name} if name else {"name": None})
        return {"name": name} if name else {"name": None}
    except IndexError:
        error = "No faces found, show face and try again"
    except ValueError:
        error = "More than one face found, remove additional faces"
    print(error)
    return {"error": error}