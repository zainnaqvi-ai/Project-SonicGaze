import cv2
import os

CAMERA_INDEX = 0    #confirm in webcam
PERSON_ID = 1       # change this number for a different person later
TARGET_COUNT = 150    # cap, you can add more in next round or quit earlier by q

if not os.path.exists('dataset'):
    os.makedirs('dataset')

existing = [f for f in os.listdir('dataset') if f.startswith(f'user.{PERSON_ID}.')]
existing_numbers = [int(f.split('.')[2]) for f in existing] if existing else []
saved_total = max(existing_numbers) if existing_numbers else 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(CAMERA_INDEX)

session_count = 0
print(f'Person {PERSON_ID} already has {saved_total} saved photo(s).')
print('SPACE = capture this frame   |   Q = stop and save')

while True:
    ret, frame = cam.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    display = frame.copy()
    for (x, y, w, h) in faces:
        cv2.rectangle(display, (x, y), (x+w, y+h), (0, 255, 0), 2)

    status = f'Session: {session_count}/{TARGET_COUNT}   Total saved: {saved_total}'
    cv2.putText(display, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(display, 'SPACE = capture   Q = quit', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow('Manual Face Capture', display)

    key = cv2.waitKey(1) & 0xFF

    if key == ord(' ') and len(faces) > 0:
        (x, y, w, h) = faces[0]
        face_crop = gray[y:y+h, x:x+w]
        saved_total += 1
        filename = f'dataset/user.{PERSON_ID}.{saved_total}.jpg'
        cv2.imwrite(filename, face_crop)
        session_count += 1
        print(f'Saved {filename}')

    if key == ord('q'):
        break
    if session_count >= TARGET_COUNT:
        break

print(f'Session done. Captured {session_count} new photo(s). Total for person {PERSON_ID}: {saved_total}.')
cam.release()
cv2.destroyAllWindows()