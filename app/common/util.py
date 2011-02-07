import random
import uuid
from app.common.models import message
from app.common.models import card

from django.shortcuts import render_to_response as render
_generate_uuid = lambda: uuid.uuid4().hex

def generate_uuid():
    return _generate_uuid()

def generate_cards():
    for x in range(100):
        serial = str(uuid.uuid4())
        pin = generate_uuid()[:16]
        value = random.choice([5000, 10000, 15000])
        x = x + x
        _card = {'serial': serial, 'pin': pin, 'value': value}
        card.save(_card)

def response(messages):
    args = {'messages': messages}
    for m in messages:
        message.msg_out_save(m)
    return render('msg.html', args)