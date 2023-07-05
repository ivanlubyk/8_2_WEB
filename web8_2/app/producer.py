import pika
from faker import Faker
from bson import ObjectId
from models import Contact
from common import mongo

fake = Faker()


credentical = pika.PlainCredentials('nufbidlm', 'sEmpyTiB3kz3E1e1SomwNQXJXdnjCo8G')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='beaver.rmq.cloudamqp.com', port=5672, credentials=credentical, virtual_host='nufbidlm')
)

channel = connection.channel()
channel.queue_declare(queue='email_queue')


def generate_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
        )
        contact.save()
        contacts.append(contact)
    return contacts


def send_contact_ids(contact_ids):
    for contact_id in contact_ids:
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact_id),
        )
        print(f"Contact ID {contact_id} sent to the email queue")



if __name__ == '__main__':
    num_contacts = 10
    contacts = generate_contacts(num_contacts)
    contact_ids = [str(contact.id) for contact in contacts]
    send_contact_ids(contact_ids)
    connection.close()
