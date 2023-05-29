from fastapi import FastAPI
from prisma import Prisma
from db import get_all_faces, add_face
from detect import get_face_encoding, check_face_in_db
from pydantic import BaseModel
from typing import List

app = FastAPI()
prisma = Prisma(auto_register=True)

class AddFaceBody(BaseModel):
    name: str
    # face_encoding: List[float]

# class GetEncodingBody(BaseModel):
#     image_array: List[List[List[int]]]

class CheckFaceBody(BaseModel):
    unknown_encoding: List[float]

@app.on_event("startup")
async def startup():
    print("startup")
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    print("shutdown")
    await prisma.disconnect()

@app.get("/faces")
async def get_faces():
    return {k:v for k,v in enumerate(await get_all_faces())}

@app.post("/face")
async def _add_face(body: AddFaceBody):
    error = ""
    try:
        face = await add_face(**body.dict())
        return face
    except IndexError:
        error = "No faces found, show face and try again"

    except ValueError:
        error = "More than one face found, remove additional faces"
    
    return {"error": error}

@app.get("/faceEncoding")
async def _get_face_enconding():
    error = ""
    try:
        enc = get_face_encoding()
        return {"success": True}
    except IndexError:
        error = "No faces found, show face and try again"
    
    except ValueError:
        error = "More than one face found, remove additional faces"
    
    return {"error": error}

@app.get("/checkFace")
async def _check_face():
    error = ""
    try:
        name = await check_face_in_db()

        return {"name": name} if name else {"name": None}
    except IndexError:
        error = "No faces found, show face and try again"
    except ValueError:
        error = "More than one face found, remove additional faces"
            
    return {"error": error}