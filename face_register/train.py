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


# video = cv2.VideoCapture(0)
# video.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

# tot_faces = int(input("Enter the number of faces you wish to register...\n"))
# face_counter = 0
# img_per_face = int(input("Enter the number of images per face you wish to click...\n"))
# img_counter = 0
# face = None
# face_labels = []

# while True:
#   if face is None:
#     face = input('\nEnter the name of the person you are registering...\n')
#     face_labels.append(face)
#     dirc = 'faces/{}'.format(face)
#     if not os.path.isdir(dirc):
#       os.mkdir(dirc)
#     img_counter = 0
#     face_counter += 1
  
#   check, frame = video.read()
#   faces = face_cascade.detectMultiScale(frame, scaleFactor=1.05, minNeighbors=3, minSize=(150, 150))

#   for x, y, w, h in faces:
#     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     face_res_112 = cv2.resize(frame[y:y+h,x:x+w,:], (112, 112))
    
#     break
  
#   cv2.imshow("video", frame)

#   key = cv2.waitKey(1)
#   if key == ord('c'):
#     frame = cv2.putText(frame, "Press 'c' again to confirm the pic, any other key to retake" , (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#     cv2.imshow("video", frame)
    
#     key = cv2.waitKey(0)
#     if key == ord('c'):
#       img_name = "face_{}.png".format(img_counter+1)
#       for i in range(5):
#         sav = aug_pipe.augment_image(face_res_112)
#         cv2.imwrite('faces/{}/{}_{}'.format(face, i, img_name), sav)
#       print("Image {} for {} written!".format(img_counter+1, face))
#       img_counter += 1
#       if img_counter == img_per_face:
#         face = None
          
#   if face_counter == tot_faces and img_counter == img_per_face:
#     break
#   if key == ord('q'):
#     break
        
# video.release()
# cv2.destroyAllWindows()

# with open('../labels/face_labels.txt', 'w') as f:
#   for name in face_labels:
#     f.write(name)
#     f.write('\n')

# embeddings = []
# face_id = []

# for idx, name in enumerate(face_labels):
#   for file in os.listdir('faces/{}'.format(name)):
#     if file[-4:] == '.png':
#       image = cv2.imread('faces/{}/{}'.format(name, file))
#       rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#       embeddings.append(get_embeddings(rgb)[0])
#       face_id.append(idx)

# classifier = SVC(kernel='rbf', probability=True)
# classifier.fit(embeddings, face_id)
# with open('../models/svc.pkl', "wb") as f:
#   f.write(pickle.dumps(classifier))
