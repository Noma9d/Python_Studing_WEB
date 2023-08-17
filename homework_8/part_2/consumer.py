import pika
import json


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="id_queue", durable=True)


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f"We send message on email from id {message}")


channel.basic_consume(queue="id_queue", on_message_callback=callback)

if __name__ == "__main__":
    channel.start_consuming()
