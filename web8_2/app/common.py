import pika
import mongoengine as mongo


uri = "mongodb+srv://userweb12:641641@cluster12.bopqszz.mongodb.net/?retryWrites=true&w=majority"
mongo.connect(host=uri)

credentical = pika.PlainCredentials('nufbidlm', 'sEmpyTiB3kz3E1e1SomwNQXJXdnjCo8G')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='beaver.rmq.cloudamqp.com', port=5672, credentials=credentical, virtual_host='nufbidlm')
)

channel = connection.channel()
channel.queue_declare(queue='email_queue')
