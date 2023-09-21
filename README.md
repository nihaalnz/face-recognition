# face-recognition

## Overview

This repository contains the code for a self-driving bus authentication system that uses facial recognition to authenticate users for check-in and check-out. The system comprises both a frontend and a backend, with the backend utilizing the Python library `dlib` and `face_recognition` for face recognition and FastAPI for the API. The frontend uses Flask to serve webcam images to the backend for recognition.

## Features

- Facial recognition for user authentication.
- User check-in and check-out functionality.
- Integration with a database for user management and tracking.
- Real-time webcam image serving and recognition.

## Prerequisites

Before running the application, make sure you have the following prerequisites installed:

- Python 3.10 or higher
- pip package manager
- Required Python packages (see the `requirements.txt` file)
- A webcam for image capture

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/nihaalnz/face-recognition
    ```
2. Navigate to the project directory:
    ```bash
    cd face-recognition
    ```
3. Create a virtual environment (recommended)
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS or Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install the required packages:

    5.1 Install the required python packages ([Requires C++ Build Tools and CMake](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)):
    ```bash
    pip install -r requirements.txt
    ```
    5.2 Install the required node packages (need to have node and npm installed):
    
    5.2.1 Navigate to frontend package (new terminal):
    
    ```bash
    cd face-recognition/frontend
    ```
    
    5.2.2 Install the npm packages:
    ```bash
    npm install
    ```

    5.2.3 Build the css using tailwind:
    ```bash
    npm run build
    ```

## Configuration

1. Configure the database connection details in `.env`.

2. Ensure that the necessary models for `dlib` and `face_recognition` are downloaded and placed in the appropriate directories. You can follow the instructions provided by these libraries for their installation.

## Usage
1. Make an .env file by filling the contents in [sample.env](/sample.env)

2. Start the backend FastAPI server:
    ```bash
    python backend
    ```
    The backend server will start at `http://localhost:8000`.

3. Start the frontend Flask server (in a separate terminal):
    ```bash
    python frontend
    ```
4. Access the application in your web browser at `http://localhost:5000`.

## Contributing

Contributions to this project are welcome! If you find a bug or have an enhancement in mind, please open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of `dlib`, `face_recognition`, FastAPI, and Flask for their excellent libraries and frameworks.
