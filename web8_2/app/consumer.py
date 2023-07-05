from models import Contact
import pika
import mongoengine as mongo


# Підключення до черги RabbitMQ
credentials = pika.PlainCredentials('nufbidlm', 'sEmpyTiB3kz3E1e1SomwNQXJXdnjCo8G')
parameters = pika.ConnectionParameters('beaver.rmq.cloudamqp.com', 5672, 'nufbidlm', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Підключення до бази даних MongoDB
mongo.connect(host="mongodb://userweb12:641641@cluster12.bopqszz.mongodb.net/mydatabase")


class Contact(mongo.Document):
    email = mongo.EmailField()
    sent = mongo.BooleanField(default=False)


def send_email(contact_id):
    # Імітація надсилання email
    print(f"Sending email to contact {contact_id}...")
    # Оновлення логічного поля контакту в базі даних на True
    contact = Contact.objects.get(id=contact_id)
    contact.sent = True
    contact.save()
    print(f"Email sent to contact {contact_id}")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    send_email(contact_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Встановлення обробника повідомлень
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

# Очікування повідомлень з черги
print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()