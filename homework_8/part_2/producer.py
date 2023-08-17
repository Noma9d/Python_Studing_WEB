from seed import seed_data
from connect_db import url
from pymongo import MongoClient
from bson import ObjectId
import pika
import json


client = MongoClient(url)
db = client.FirstMongoDB

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="email_task", exchange_type="direct")
channel.queue_declare(queue="email_queue", durable=True)
channel.queue_bind(exchange="email_task", queue="email_queue")

channel.exchange_declare(exchange="sms_task", exchange_type="direct")
channel.queue_declare(queue="sms_queue", durable=True)
channel.queue_bind(exchange="sms_task", queue="sms_queue")

channel.exchange_declare(exchange="id_task", exchange_type="direct")
channel.queue_declare(queue="id_queue", durable=True)
channel.queue_bind(exchange="id_task", queue="id_queue")


def main():
    seed_data(100)

    data = db.contact.find()

    for el in data:
        channel.basic_publish(
            exchange="id_task",
            routing_key="id_queue",
            body=json.dumps(f'{el["_id"]}').encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        channel.basic_publish(
            exchange="email_task",
            routing_key="email_queue",
            body=json.dumps(f'{el["email"]}').encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        channel.basic_publish(
            exchange="sms_task",
            routing_key="sms_queue",
            body=json.dumps(f'{el["phone_number"]}').encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

        db.contact.update_one(
            {"_id": ObjectId(f'{el["_id"]}')}, {"$set": {"send_status": "True"}}
        )


if __name__ == "__main__":
    main()
