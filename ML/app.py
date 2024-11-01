import torch
from flask import Flask, render_template, request, redirect, url_for, Response
import cv2
import face_recognition
import numpy as np
import sqlite3
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite setup
def create_database():
    conn = sqlite3.connect('known_faces.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS KnownFaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# Load known face encodings from the database
known_face_encodings = []
known_face_names = []

def load_known_faces():
    global known_face_encodings, known_face_names
    conn = sqlite3.connect('known_faces.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, encoding FROM KnownFaces')
    rows = cursor.fetchall()
    conn.close()
    known_face_names = [row[0] for row in rows]
    known_face_encodings = [np.frombuffer(row[1], dtype=np.float64) for row in rows]

# Index page
@app.route('/')
def index():
    return render_template('index.html')

# Upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['file']
        if file:
            image = face_recognition.load_image_file(file)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                face_encoding = face_encodings[0]
                save_face_to_db(name, face_encoding)
                return redirect(url_for('index'))
    return render_template('upload.html')

# Save face encoding and name to SQLite
def save_face_to_db(name, face_encoding):
    encoding_blob = face_encoding.tobytes()
    conn = sqlite3.connect('known_faces.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO KnownFaces (name, encoding) VALUES (?, ?)', (name, encoding_blob))
    conn.commit()
    conn.close()

# Video feed generator
def generate_video_feed():
    video_capture = cv2.VideoCapture(0)
    load_known_faces()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            face_encoding = torch.tensor(face_encoding).to(device)

            # Use cosine similarity or distance calculations on GPU
            distances = [
                torch.dist(face_encoding, torch.tensor(encoding).to(device)).item()
                for encoding in known_face_encodings
            ]
            min_distance = min(distances)
            name = "Unknown"
            if min_distance < 0.6:
                first_match_index = distances.index(min_distance)
                name = known_face_names[first_match_index]

            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    video_capture.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Make it accessible on all network interfaces
