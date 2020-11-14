import os
import json
from kafka import KafkaProducer
import json
from datetime import date
import time
import sys
from keras.models import load_model
import argparse
import pickle
import glob
import cv2
import subprocess

user_id1 = sys.argv[1]
path_name = "/home/pi/hx711py/Project/"
today = str(date.today())
timestamp = int(time.time())


EMULATE_HX711=False
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(449)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")

ck_list = []
i=1

while True:
    if i > 10:
        break
    try:
        i += 1
        val = max(0, int(hx.get_weight()))
        print(val)

        if val >= 10:
            ck_list.append(val)
            print('gathering data: {}'.format(ck_list))
        
        if len(ck_list) >= 3:
            err = (ck_list[-1] - ck_list[-2]) / ck_list[-1]
            if err >= 0.03:
                pass
            else:  
                print(val) #final output
                
                file_name = "{}_{}.jpg".format(today,i)
                p = subprocess.getoutput("sudo fswebcam --no-banner -r 640x360 -S 10 -d /dev/video0 /home/pi/hx711py/Project/image/{}.jpg --no-banner".format(timestamp)) 
                print(p)
                
                hx.power_down()
                break
                

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()



b = glob.glob('/home/pi/hx711py/Project/image/{}.jpg'.format(timestamp))[-1]
image = cv2.imread(b)
output = image.copy()
image = cv2.resize(image, (32, 32))




image = image.astype("float") / 255.0


image = image.flatten()
image = image.reshape((1, image.shape[0]))


print("-----read_model-------")
model = load_model('/home/pi/hx711py/Project/simple_nn3.h5')
lb = pickle.loads(open('/home/pi/hx711py/Project/simple_nn_lb3.pickle', "rb").read())


preds = model.predict(image)


i = preds.argmax(axis=1)[0]
label = lb.classes_[i]
print('result:',label)
print("{},{},{}".format(user_id1,label,val))
with open(path_name + "result/{}.txt".format(timestamp),"a") as f:
     f.write("{},{},{}".format(user_id1,label,val))


topic = "iot"
broker_list = 'localhost:9092'

producer = KafkaProducer(bootstrap_servers=broker_list,
        value_serializer=lambda m: json.dumps(m).encode('utf8'))
message = {'user_id':user_id1,'food_name':label,'food_weight':val}
while True:
    producer.send(topic, message)
    producer.flush()
    time.sleep(3)



