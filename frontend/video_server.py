from flask import Flask, render_template, Response
import cv2
import threading

app = Flask(__name__)
camera = cv2.VideoCapture(0)
camera_lock = threading.Lock()


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/video_feed")
def video_feed():
    with camera_lock:
        return Response(
            generate(), mimetype="multipart/x-mixed-replace; boundary=frame"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
