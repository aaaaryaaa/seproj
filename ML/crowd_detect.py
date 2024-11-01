import cv2
import numpy as np
import time
from yolov5 import YOLOv5

# Initialize YOLO for person detection
yolo = YOLOv5('yolov5s.pt', device='cpu')

video_capture = cv2.VideoCapture(0)

# Time interval to check for crowd gathering (in seconds)
time_interval = 2  
# Threshold for rapid crowd gathering (e.g., increase by 5 people)
crowd_gather_threshold = 5  

# Count of people in previous check
prev_count = 0  
# Timestamp of the last check
prev_time = time.time()

def detect_people(frame):
    # Use YOLO to detect people in the frame
    results = yolo.predict(frame)
    people_count = sum(1 for result in results if result['class'] == 'person')
    return people_count

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Detect people in the current frame
    people_count = detect_people(frame)
    
    current_time = time.time()

    # Check if time interval has passed
    if current_time - prev_time > time_interval:
        # Calculate the change in number of people
        count_change = people_count - prev_count

        if count_change >= crowd_gather_threshold:
            print("Crowd gathering detected!")
            # You can trigger an alert or flag this event

        # Update for the next interval
        prev_count = people_count
        prev_time = current_time

    # Display the frame with people count
    cv2.putText(frame, f'People Count: {people_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Crowd Gathering Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
