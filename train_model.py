import cv2
import os
import numpy as np

if not os.path.exists('trainer'):
    os.makedirs('trainer')

recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for image_path in image_paths:
        gray_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        gray_img = cv2.equalizeHist(gray_img)
        person_id = int(os.path.split(image_path)[-1].split('.')[1])
        face_samples.append(gray_img)
        ids.append(person_id)
    return face_samples, ids

print('Training... please wait.')
faces, ids = get_images_and_labels('dataset')
recognizer.train(faces, np.array(ids))
recognizer.save('trainer/trainer.yml')

print(f'Done. Trained on {len(np.unique(ids))} unique person(s), {len(faces)} total images.')