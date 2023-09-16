from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, Response, request
import cv2, base64, requests, os, threading

BASE_API_URL = os.getenv("BASE_API_URL")

app = Flask(__name__)
camera = cv2.VideoCapture(
    int(os.getenv("VIDEO_URL"))
    if len(os.getenv("VIDEO_URL")) == 1
    else os.getenv("VIDEO_URL")
)
camera_lock = threading.Lock()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


def generate():
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, jpeg = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )


def capture_frame():
    with camera_lock:
        success, frame = camera.read()
        if success:
            ret, jpeg = cv2.imencode(".jpg", frame)
            if ret:
                # Convert the frame to base64 for sending to the client
                frame_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")
                return frame_base64


@app.route("/video_feed")
def video_feed():
    with camera_lock:
        return Response(
            generate(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )


@app.route("/_check_face", methods=["GET"])
def check_face():
    image_base64 = capture_frame()
    bus_id = os.getenv("BUS_ID")
    return requests.get(
        f"{BASE_API_URL}/check-face",
        json={"image_encoding": image_base64, "bus_id": bus_id},
    ).json()


@app.route("/_register", methods=["POST"])
def add_face():
    data = request.json
    image_base64 = capture_frame()
    return requests.post(
        f"{BASE_API_URL}/add-face",
        json={"image_encoding": image_base64, "name": data["name"]},
    ).json()


@app.route("/_capacity", methods=["GET"])
def get_capacity():
    bus_id = os.getenv("BUS_ID")
    return requests.get(f"{BASE_API_URL}/capacity", json={"bus_id": bus_id}).json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
