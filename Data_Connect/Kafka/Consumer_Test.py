
from Project_Kafka.Consumer_Setting import KafkaConsumer

topic_name = 'test'
test = KafkaConsumer(topic_name)
consumer = test.consumer_init()

# 迴圈是持續收資料的必須關鍵。
while True:
    try:
        data = test.consumer_start(consumer)
        time, key, value = test.data_of_message(data)
        print(time, key, value)
    except TypeError: continue
    except Exception as e: print(e)





