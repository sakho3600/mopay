import random
import uuid

from models import Card

from django.shortcuts import render_to_response as render
_generate_uuid = lambda: uuid.uuid4().hex

def generate_uuid():
    return _generate_uuid()

def generate_cards():
    x = 0
    while x < 100:
        serial = str(uuid.uuid4())
        pin = generate_uuid()[:16]
        value = random.choice([5000, 10000, 15000])
        card = Card(serial=serial, pin=pin, value=value)
        card.save()
        x = x + 1

def response(messages):
    args = {'messages': messages}
    for m in messages:
        m.save()
    return render('msg.html', args)