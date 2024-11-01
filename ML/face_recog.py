import cv2
import numpy as np
import face_recognition
import sqlite3

# SQLite setup
def create_database():
    conn = sqlite3.connect('known_faces.db')
    cursor = conn.cursor()
    # Create the table if it doesn’t exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS KnownFaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database
create_database()

# Load known face encodings from the SQLite database
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

# Load known faces from the database
load_known_faces()

# Start capturing video
video_capture = cv2.VideoCapture(0)
frame_skip_count = 3  # Process every 3rd frame for efficiency
frame_counter = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Process every frame_skip_count frame for efficiency
    if frame_counter % frame_skip_count == 0:
        # Resize and convert the frame
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    frame_counter += 1

    # Draw rectangles and labels on the frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
