# AUM SHREEGANESHAAYA NAMAH|| AUM SHREEHANUMATE NAMAH||
import cv2
import os
import pickle
from .face_aug import aug_pipe
from .face_tflite import get_embeddings
from sklearn.svm import SVC
from base64 import b64decode

face_cascade = cv2.CascadeClassifier()
face_cascade.load('models/haarcascade_frontalface_default.xml')

def startTraining(trainData):
  try:
    print("Starting Training.")
    # N students, M images per student
    # { "train" : [
    #   { "name" : "imisra", "files" : ['..', '..'] },
    #   { "name" : "tulika", "files" : ['..', '..'] },
    # ] }
    # req = requests.post("http://localhost:5000/register", json=td)
    # req.content.decode("UTF-8")

    img_per_face = len(trainData[0]["files"])
    face_labels = [ td["name"] for td in trainData ]

    for i_face, face in enumerate(face_labels):
      if not os.path.isdir(f"face_register/faces/{face}"): os.mkdir(f"face_register/faces/{face}")
      imgs = trainData[i_face]["files"]

      for i_img, img_b64 in enumerate(imgs):
        imgPath = f"face_register/faces/{face}/{face}_{i_img}.png"
        imgFile = open(imgPath, "wb")
        imgFile.write(b64decode(img_b64))
        imgFile.close()

        img = cv2.imread(imgPath)
        _faces = face_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=3, minSize=(150, 150))
        if len(_faces) < 1: continue

        x, y, w, h = _faces[0]
        frame = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        face_res_112 = cv2.resize(frame[y:y+h,x:x+w,:], (112, 112))

        for i_aug in range(5): # Augmenting Images (5 per image)
          sav = aug_pipe.augment_image(face_res_112)
          cv2.imwrite(f"face_register/faces/{face}/{face}_{i_img}_{i_aug}.png", sav)
      
    with open('labels/face_labels.txt', 'w') as f:
      for name in face_labels:f.write(f"{name}\n")

    embeddings, face_id = [], []

    for i_face, face in enumerate(face_labels):
      for i_img in range(img_per_face):
        for i_aug in range(5):
          img = cv2.imread(f"face_register/faces/{face}/{face}_{i_img}_{i_aug}.png")
          rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          embeddings.append(get_embeddings(rgb)[0])
          face_id.append(i_face)

    classifier = SVC(kernel='rbf', probability=True)
    classifier.fit(embeddings, face_id)
    with open('models/svc.pkl', "wb") as f: f.write(pickle.dumps(classifier))

    print("Completed Training.")
  except:
    print("Problem in training. Aborted.")
