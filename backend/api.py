from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from db import (
    get_all_faces,
    add_face_in_db,
    check_passenger_in_bus,
    add_passenger_in_bus,
    remove_passenger_from_bus,
    get_capacity,
)
from detect import get_face_encoding, check_face_in_db, decode_image_to_array
from pydantic import BaseModel

app = FastAPI()
prisma = Prisma(auto_register=True)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


class AddFaceBody(BaseModel):
    name: str
    image_encoding: str


class GetEncodingBody(BaseModel):
    image_encoding: str


class ImageData(BaseModel):
    image_encoding: str
    bus_id: int


class CapacityBody(BaseModel):
    bus_id: int


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
async def add_face(body: AddFaceBody):
    error = ""
    try:
        image_encoding = decode_image_to_array(body.image_encoding)
        face = await add_face_in_db(body.name, image_encoding)
        if isinstance(face, str):
            error = "Face already exists in the database"
        else:
            return face
    except IndexError:
        error = "No faces found, show face and try again"

    except ValueError:
        error = "More than one face found, remove additional faces"

    return HTTPException(status_code=500, detail=error)


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
async def check_face(image: ImageData):
    error = ""
    try:
        image_array = decode_image_to_array(image.image_encoding)
        id = await check_face_in_db(image_array)
        if isinstance(id, int):
            passenger_in_bus = await check_passenger_in_bus(id, image.bus_id)
            if passenger_in_bus:
                user = await remove_passenger_from_bus(id, image.bus_id)
                status = "checked out"
            else:
                capacity = await get_capacity(image.bus_id)
                if capacity == 0:
                    raise ValueError(
                        "Bus has reached its <strong>maximum capacity</strong>"
                    )

                user = await add_passenger_in_bus(id, image.bus_id)
                status = "checked in"
            return {"name": user.name, "status": status}
        else:
            error = "Face <strong>not found in database</strong>, <strong>add face</strong> first"
    except IndexError:
        error = "No faces found, show face and try again"
    except ValueError as e:
        error = e.__str__()
    return HTTPException(status_code=500, detail=error)


@app.get("/capacity")
async def _get_capacity(capacity: CapacityBody):
    capacity = await get_capacity(capacity.bus_id)
    return {"capacity": capacity}
