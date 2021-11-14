# AUM SHREEGANEHSAAYA NAMAH||
import cv2
import numpy as np
from face_tflite import get_embeddings, face_classifier
from mask_tflite import classify_mask

def load_labels(path):
  with open(path, 'r') as f:
    return {i: line.strip() for i, line in enumerate(f.readlines())}

mask_labels = load_labels('labels/mask_labels.txt')
face_labels = load_labels('labels/face_labels.txt')

face_cascade = cv2.CascadeClassifier()
face_cascade.load('models/haarcascade_frontalface_default.xml')

acc_thresh_mask = 0.8
acc_thresh_face = 0.8


def detectFaceAndMask(framePath):
  frame = cv2.imread(framePath)
  rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  faces = face_cascade.detectMultiScale(rgb, scaleFactor=1.05, minNeighbors=3, minSize=(150, 150))
  if len(faces) < 1: return None

  x, y, w, h = faces[0]
  mask_res_224 = cv2.resize(rgb[y:y+h,x:x+w,:], (224, 224))
  mask_probs = classify_mask(mask_res_224)
  mask_id = np.argmax(mask_probs)
  _prob = mask_probs[0][mask_id]
  mask_info = {
    "maskLabel" : (mask_labels[mask_id] if (_prob > acc_thresh_mask) else 'unsure'),
    "probability" : _prob
  }
  cv2.destroyAllWindows()
  return mask_info


def recognizeFace(framePath):
  frame = cv2.imread(framePath)
  rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  faces = face_cascade.detectMultiScale(rgb, scaleFactor=1.05, minNeighbors=3, minSize=(150, 150))
  if len(faces) < 1: return None

  x, y, w, h = faces[0]
  face_res_112 = cv2.resize(rgb[y:y+h,x:x+w,:], (112, 112))
  embedding = get_embeddings(face_res_112)[0]
  face_probs = face_classifier.predict_proba([embedding])[0]
  face_id = np.argmax(face_probs)
  _prob = face_probs[face_id]
  face_info = {
    "faceLabel": face_labels[face_id] if (_prob > acc_thresh_face) else 'unknown',
    "probability" : _prob
  }
  cv2.destroyAllWindows()
  return face_info


if __name__ == "__main__":
  test_images = [
    "test_images/tulika.jpg",
    "test_images/imisra.jpg",
    "test_images/imisra_0.jpg",
    "test_images/imisra_1.jpg",
    "test_images/imisra_2.jpg",
    "test_images/imisra_3.jpg",
    "test_images/none.jpg",
  ]
  for ti in test_images:
    print(f"{ti} : {detectFaceAndMask(ti)}")
