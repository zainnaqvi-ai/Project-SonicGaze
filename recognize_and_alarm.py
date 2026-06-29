import cv2
import serial
import time

CAMERA_INDEX = 0       # same index confirmed
ARDUINO_PORT = 'COM8'  # the exact COM port

arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
time.sleep(2)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

COUSIN_ID = 1
CONFIDENCE_THRESHOLD = 45

cam = cv2.VideoCapture(CAMERA_INDEX)
print('Watching for cousin... press Q to quit.')

while True:
    ret, frame = cam.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    match_found = False
    for (x, y, w, h) in faces:
        face_crop = gray[y:y + h, x:x + w]
        predicted_id, confidence = recognizer.predict(face_crop)

        if predicted_id == COUSIN_ID and confidence < CONFIDENCE_THRESHOLD:
            match_found = True
            label, color = f'Zain ({confidence:.0f})', (0, 0, 255)
        else:
            label, color = f'Unknown ({confidence:.0f})', (0, 255, 0)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    arduino.write(b'1' if match_found else b'0')

    cv2.imshow('Face Recognition Alarm', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

arduino.write(b'0')
cam.release()
cv2.destroyAllWindows()
arduino.close()
