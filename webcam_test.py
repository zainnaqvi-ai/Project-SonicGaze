import cv2

cam = cv2.VideoCapture(0)  # 0 = default webcam
print('Press Q in the window to quit.')

while True:
    ret, frame = cam.read()
    if not ret:
        print('Could not read from camera. Is another application using it?')
        break

    cv2.imshow('Webcam Test', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()