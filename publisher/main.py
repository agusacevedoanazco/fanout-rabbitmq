import pika
from flask import Flask, jsonify, request, abort
import os

rmquser = os.getenv("RABBITMQ_USER",default="demo")
rmqpass = os.getenv("RABBITMQ_PASS",default="demo")
rmqhost = os.getenv("RABBITMQ_HOST",default="localhost")
rmqport = os.getenv("RABBITMQ_PORT",default=5672)
rmqvhost = os.getenv("RABBITMQ_VHOST",default="/sub")
rmqxch = os.getenv("RABBITMQ_EXCHANGE",default="demoexchange")

app = Flask(__name__)

@app.route("/pub",methods=["POST"])
def sendmessage():
    if request.method=="POST":
        data = request.get_json()
        return jsonify(str("publica2")) if publish_message(data=data['msg']) == True else abort(404)

#publish message
def publish_message(data):
    if data != None:
        channel.basic_publish(exchange=rmqxch,routing_key="",body=data)
        return True
    else:
        return False

if __name__ == '__main__':
    #set connection params
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
    #create connection
    channel = connection.channel()
    #declare exchange
    channel.exchange_declare(
        exchange=rmqxch,
        exchange_type="fanout")
    app.run()
