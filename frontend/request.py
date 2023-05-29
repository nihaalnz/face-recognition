from dotenv import load_dotenv
load_dotenv()

import requests, os
from typing import List
import time

BASE_API_URL = os.getenv("BASE_API_URL")

def get_face_encoding() -> str | List[float]:
    req = requests.get(f"{BASE_API_URL}/faceEncoding")

    body = req.json()
    error = body.get("error")
    return error if error is not None else []

def check_face() -> str | None:
    req = requests.get(f"{BASE_API_URL}/checkFace")
    
    body = req.json()
    error = body.get("error")
    return error if error else req.json().get("name")

def add_face(name: str):
    req = requests.post(f"{BASE_API_URL}/face", json={"name": name})

    return req.json()

if __name__ == "__main__":
    cur = time.time()
    print(check_face())
    print(time.time() - cur)