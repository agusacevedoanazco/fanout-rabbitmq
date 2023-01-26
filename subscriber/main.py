import pika
import os

rmquser = os.getenv("RABBITMQ_USER",default="demo")
rmqpass = os.getenv("RABBITMQ_PASS",default="demo")
rmqhost = os.getenv("RABBITMQ_HOST",default="localhost")
rmqport = os.getenv("RABBITMQ_PORT",default=5672)
rmqvhost = os.getenv("RABBITMQ_VHOST",default="/sub")
rmqxch = os.getenv("RABBITMQ_EXCHANGE",default="demoexchange")
subnum = os.getenv("SUBNUM",1)

def callback(ch, method, properties, body):
    print("Received: {}".format(body))

if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rmqhost,
            port=rmqport,
            virtual_host=rmqvhost,
            credentials=pika.PlainCredentials(
                username=rmquser,
                password=rmqpass)
            )
        )
    channel = connection.channel()
    channel.exchange_declare(exchange=rmqxch,exchange_type="fanout")
    result = channel.queue_declare(queue=str("myqueue"+str(subnum)),exclusive=False)
    queue_name = result.method.queue
    # bind the queue
    channel.queue_bind(exchange=rmqxch,queue=queue_name)
    # consume the queue data
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Listening data on queue: myqueue"+str(subnum))
    channel.start_consuming()