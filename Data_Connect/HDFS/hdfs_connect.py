from hdfs.client import Client, InsecureClient
import redis
import json
# r = redis.StrictRedis(host='192.168.1.176', port=6379,decode_responses=True)

client = InsecureClient("http://192.168.1.176:50070", user='spark')
# 路徑不用hdfs://
# client.list("/") -> ['recipe', 'tmp', 'user']


with client.read("/recipe/recipe1018_V8.json")as reader:
    data = json.load(reader)

print(data[:10])