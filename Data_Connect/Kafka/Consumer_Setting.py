

from confluent_kafka import Consumer

class KafkaConsumer(object):
    def __init__(self, topic_name):
        self.topic_name = topic_name

    # 接收error訊息
    def error_cb(self,err):
        print('Error: %s' % err)

    # 轉換msgKey或msgValue成為utf-8的字串
    def try_decode_utf8(self,data):
        if data: return data.decode('utf-8')
        else: return None

    # 當發生commit時被呼叫
    def on_commit(self,err, partitions):
        if err: print(f'Failed to commit offsets: {err}')
        else: pass

    # 當發生Re-balance時, 如果有partition被assign時被呼叫
    def print_assignment(self,consumer, partitions):
        result = '[{}]'.format(','.join([p.topic + '-' + str(p.partition) for p in partitions]))
        print('Setting new partitions:', result)

    # 當Re-balance被觸發後, Commit現在process的offets
    def commit_on_revoke(self,consumer, partitions):
        for item in self.offsets_dict.values():
            consumer.commit(item)  # 進行異步的commit
        print('Commited before rebalance.')

    def consumer_init(self):
        kafka_client = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': '123',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
            'auto.commit.interval.ms': 5000,
            'on_commit': self.on_commit,
            'error_cb': self.error_cb
        }
        consumer = Consumer(kafka_client)
        consumer.subscribe([self.topic_name],
                           on_assign=self.print_assignment,
                           on_revoke=self.commit_on_revoke)
        return consumer

    def setting_of_record(self,record):
        try:
            topic = record.topic()
            partition = record.partition()
            offset = record.offset()
            return topic, partition, offset
        except Exception as e: return e

    def data_of_message(self, record):
        try:
            timestamp = record.timestamp()
            msg_key = self.try_decode_utf8(record.key())
            msg_value = self.try_decode_utf8(record.value())
            # print(f'topic:{self.topic}, time:{self.timestamp[-1]}, ({self.msg_key}: {self.msg_value})')
            return timestamp[-1], msg_key, msg_value
        except Exception as e: return e

    def consumer_start(self,consumer):
        try:
            record_list = consumer.consume(num_messages=1, timeout=10.0)
            if not record_list: return 'NO message'
            for record in record_list:
                if record: return record
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
        except Exception as e:
            print(e)


