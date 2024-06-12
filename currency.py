from ultralytics import YOLO
import cv2
import math
import pyttsx3
import gpiod

import geocoder
#import tensorflow as tf

#interpreter = tf.lite.Interpreter(model_path="model.tflite")
#interpreter.allocate_tensors()

#input_details = interpreter.get_input_details()
#output_details = interpreter.get_output_details()

BUTTON_PIN = 27
chip = gpiod.Chip('gpiochip4')

button_line = chip.get_line(BUTTON_PIN)

button_line.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN)

engine=pyttsx3.init()

def speak(t):
    engine.say(t)
    engine.runAndWait()

model = YOLO("best.pt")
classNames = ["10 rupee","100 rupee","20 rupee","200 rupee","2000 rupee","500 rupee"]

prev_value=""
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
while True:
    success, img = cap.read()
    button_state = button_line.get_value()
    if button_state==1:
        lt,lg=gps.gps()
        if lt==0:
            g = str(geocoder.ip('me'))
        else:
            g=str(lt)+","+str(lg)
            gsm.sendSMS("9995234163",g)
            
    results = model(img, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            confidence = math.ceil((box.conf[0]*100))/100
            if confidence>0.8:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
                cls = int(box.cls[0])
                org = [x1, y1-10]
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (0, 255, 0)
                thickness = 2
                cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
                if prev_value==classNames[cls]:
                    frame_count+=1
                else:
                    frame_count=0
                if frame_count>=7:
                    frame_count=0


                    image = img[y1:y2,x1:x2]

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
                    pp=np.argmax(output_data)
                    if pp==1:
                        ttt=classNames[cls]+ " genuine note"
                        speak(ttt)
                    else:
                        speak(classNames[cls])
                    
                prev_value=classNames[cls]
    cv2.imshow('Result', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
