from kafka import KafkaProducer
import Producer_Setting
import json

topic_name = 'test'
test = KafkaProducer(topic_name)
producer = test.procuder_init()

# kafka的value可以直接讀取json，開啟檔案逐行寫入即可。
# with open(xxxx.json) as file
for i in range(100):
    data_json = {'id': '12345', 'name': 'Hank', 'sex': 'male', 'age': '18'}
    data_json = json.dumps(data_json)
    test.producer_strat(producer, i, data_json)

test.producer_flush(producer)