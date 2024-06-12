import numpy as np
import tensorflow as tf
import cv2

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

image_path = r"D:\project\23-24\fakeCurrency\dataset\Indian Currency Dataset\test\fake\821078-44998-xgbtzfrwwn-1478662483.jpg"
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Image not loaded properly")
input_shape = input_details[0]['shape']

resized_image = cv2.resize(image, (input_shape[2], input_shape[1]))

if input_details[0]['dtype'] == np.float32:
    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)


resized_image = resized_image.astype(np.float32) / 255.0

input_data = np.expand_dims(resized_image, axis=0)

if input_details[0]['dtype'] == np.float32:
    input_data = input_data.astype(np.float32)
else:
    input_data = input_data.astype(np.uint8)

interpreter.set_tensor(input_details[0]['index'], input_data)

interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])
print(output_data)
