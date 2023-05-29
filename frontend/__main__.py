from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import cv2, os
from PIL import Image, ImageTk
from request import get_face_encoding, check_face, add_face
import threading
from queue import Queue, Empty


class LoginThread(threading.Thread):
    def __init__(self, queue, args=()):
        super().__init__()
        self.queue = queue
        self.args = args

    def run(self):
        frame = self.args[0]
        status = get_face_encoding()
        if isinstance(status, list):
            self.queue.put(check_face())
        else:
            messagebox.showerror("Error", status)
            frame.prog_bar.stop()


class RegisterThread(threading.Thread):
    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        frame = self.args[1]
        res = _check_image(frame)
        if res:
            if res[0]:
                frame.prog_bar.stop()
                return messagebox.showerror(
                    "User exists!", "User is already registered!"
                )

            # face_encoding = res[-1]
            add_face(self.args[0])
            frame.prog_bar.stop()

            messagebox.showinfo("Success!", "Successfully linked face!")
            self.args[2].delete(0, "end")


root = Tk()
root.title("User recognition")
vid = cv2.VideoCapture(
    int(os.getenv("VIDEO_URL"))
    if len(os.getenv("VIDEO_URL")) == 1
    else os.getenv("VIDEO_URL")
)
w, h = 640, 480
vid.set(cv2.CAP_PROP_FRAME_WIDTH, w)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
rep = None


def read_camera(video_label):
    global rep
    _, frame = vid.read()
    # print("Running")
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo_image = ImageTk.PhotoImage(Image.fromarray(image))

    video_label.ref = photo_image
    video_label.config(image=photo_image)

    rep = root.after(10, read_camera, video_label)


def add_user():
    name = name_entry.get()
    if name:
        register_page.prog_bar.start()
        RegisterThread(args=(name, register_page, name_entry)).start()
        # res = check_image(top)
        # # print(res)
        # if res:
        #     if res[0]:
        #         return messagebox.showerror(
        #             "User exists!", "User is already registered!", parent=top
        #         )

        #     face_encoding = res[-1]
        #     add_face(name, face_encoding)
        #     messagebox.showinfo("Success!", "Successfully linked face!")
        # name_entry.delete(0, "end")
    else:
        messagebox.showwarning("Warning!", "Enter a name first to register the user!")


def check_image(top) -> tuple | None:
    top.prog_bar.start()

    def process_queue():
        try:
            res = q.get_nowait()
            if res is not None:
                name = res
                messagebox.showinfo("Logged in!", f"Successfully logged in {name}")
            else:
                messagebox.showerror(
                    "Error!",
                    "Such user not found, register if new user! Or use the card",
                )

            top.prog_bar.stop()
        except Empty:
            top.after(100, process_queue)

    q = Queue()
    LoginThread(q, args=(top,)).start()
    # status = get_face_encoding()

    # if isinstance(status, list):
    #     name = check_face()
    #     return name, status  # Possibly (None, unknown_image)
    # else:
    #     messagebox.showerror("Error", status, parent=top)

    top.after(100, process_queue)


def _check_image(top):
    status = get_face_encoding()

    if isinstance(status, list):
        name = check_face()

        return name, status  # Possibly (None, unknown_image)
    else:
        messagebox.showerror("Error", status)
        top.prog_bar.stop()


def verify():
    res = check_image(login_page)
    # print(res)
    if res:
        if res[0]:
            name = res[0]
            messagebox.showinfo("Logged in!", f"Successfully logged in {name}")
        else:
            messagebox.showerror("Error!", "Such user not found, register if new user!")


def ret_home():
    home_page.tkraise()
    if rep:
        root.after_cancel(rep)


home_page = Frame(root, width=800, height=900)
home_page.grid(row=0, column=0, sticky="news")
home_page.pack_propagate(0)

login_page = Frame(root, width=800, height=900)
login_page.grid(row=0, column=0, sticky="news")
login_page.pack_propagate(0)

video_label_1 = Label(login_page)
video_label_1.pack()

Button(login_page, text="Verify", command=verify).pack()
login_page.prog_bar = ttk.Progressbar(
    login_page, mode="indeterminate", orient="horizontal", length=200
)
login_page.prog_bar.pack()
Button(login_page, text="Go back", command=ret_home).pack()

register_page = Frame(root, width=800, height=900)
register_page.grid(row=0, column=0, sticky="news")
register_page.pack_propagate(0)

Label(register_page, font=(0, 21), text="Enter name").pack()

name_entry = Entry(register_page, font=(0, 21))
name_entry.pack(pady=5)

video_label_2 = Label(register_page)
video_label_2.pack()

# read_camera(video_label)
register_page.btn = Button(register_page, text="Register", command=add_user)
register_page.btn.pack()

register_page.prog_bar = ttk.Progressbar(
    register_page, mode="indeterminate", orient="horizontal", length=200
)
register_page.prog_bar.pack()
Button(register_page, text="Go back", command=ret_home).pack()


Button(
    home_page,
    text="Login",
    command=lambda: [login_page.tkraise(), read_camera(video_label_1)],
    width=25,
    font=(0, 16),
).pack(pady=(10, 5))
Button(
    home_page,
    text="Register",
    command=lambda: [register_page.tkraise(), read_camera(video_label_2)],
    width=25,
    font=(0, 16),
).pack(pady=(5, 10))
Button(
    home_page,
    text="Exit",
    command=root.destroy,
    width=25,
    font=(0, 16),
).pack(pady=(5, 10))

home_page.tkraise()

root.mainloop()
