import uvicorn
from api import app

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", app=app)