import tensorflow as tf
import numpy as np

interpreter = tf.lite.Interpreter('models/mobnetv2_mask.tflite')
interpreter.allocate_tensors()

def set_input_tensor_mask(input):
    input_details = interpreter.get_input_details()[0]
    tensor_index = input_details['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.uint8(input)

def classify_mask(input):
    set_input_tensor_mask(input)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = interpreter.get_tensor(output_details['index'])
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)
    return output