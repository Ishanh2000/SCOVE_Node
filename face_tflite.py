import tensorflow as tf
import numpy as np
import pickle

interpreter = tf.lite.Interpreter('models/mobilefacenet.tflite')
interpreter.allocate_tensors()
face_classifier = pickle.loads(open('models/svc.pkl', "rb").read())

def set_input_tensor_face(input):
    input_details = interpreter.get_input_details()[0]
    tensor_index = input_details['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.float32((input-127.5)/127.5)

def get_embeddings(input):
    set_input_tensor_face(input)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = interpreter.get_tensor(output_details['index'])
    return output