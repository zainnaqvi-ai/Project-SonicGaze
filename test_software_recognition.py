import cv2

CAMERA_INDEX = 0
COUSIN_ID = 1
CONFIDENCE_THRESHOLD = 45 # tune this number while watching results below

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(CAMERA_INDEX)
print('Software-only recognition test -- no Arduino involved. Press Q to quit.')

while True:
    ret, frame = cam.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_crop = gray[y:y+h, x:x+w]
        face_crop = cv2.equalizeHist(face_crop)   # matches train_model.py's preprocessing
        predicted_id, confidence = recognizer.predict(face_crop)

        if predicted_id == COUSIN_ID and confidence < CONFIDENCE_THRESHOLD:
            label = f'MATCH: Zain ({confidence:.0f})'
            color = (0, 0, 255)
            print(f'>>> ALARM WOULD FIRE NOW -- confidence {confidence:.0f}')
        else:
            label = f'Unknown ({confidence:.0f})'
            color = (0, 255, 0)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('Recognition Test (no Arduino)', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()