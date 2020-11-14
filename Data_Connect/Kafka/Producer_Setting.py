from kafka.confluent import Producer
import time
import json

class KafkaProducer(object):
    def __init__(self, topic_name):
        self.topic_name = topic_name
        self.time_start = time.time()

    # 接收error訊息
    def error_cb(self, err):
        print('Error: %s' % err)

    # 轉換msgKey或msgValue成為utf-8的字串
    def try_decode_utf8(self, data):
        if data: return data.decode('utf-8')
        else: return None

    def delivery_callback(self, err, msg):
        if err: print(err)
        else:
            if int(msg.key()) % 10 == 0:
                print(f'{msg}Message delivered to topic:[{self.topic_name}]\n')

    def procuder_init(self):
        kafka_client = {
            'bootstrap.servers': '192.168.196.116:9092',
            'max.in.flight.requests.per.connection':1,
            'error_cb': self.error_cb
        }
        procuder = Producer(kafka_client)
        return procuder

    def producer_strat(self,producer,key,value):
        try:
            # 每一行或每個json，發送一次訊息。
            # 呼叫poll來讓client程式去檢查內部的Buffer, 並觸發callback
            producer.produce(self.topic_name, key=str(key), value=value)
            producer.poll(0)

        except BufferError as e:
            print(f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again\n')
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
        except Exception as e:
            print(e)

    def producer_flush(self, producer):
        # 計算訊息量與時間
        time_spend = time.time() - self.time_start
        print('Send        : ' + str(100) + ' messages to Kafka')
        print('Total spend : ' + str(time.strftime('%H:%M:%S', time.gmtime(time_spend))))
        print('Throughput : ' + str(100 / time_spend) + ' msg/sec')

        producer.flush(10)
        print('Message sending completed!')


