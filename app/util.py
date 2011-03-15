import random
import uuid
import pyDes

import settings
from models import Card

from django.shortcuts import render_to_response as render
_generate_uuid = lambda: uuid.uuid4().hex

#k = pyDes.des("DESCRYPT", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
des = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", 
              pad=None, padmode=pyDes.PAD_PKCS5)

FILE_TYPE_NOT_SUPPORTED = "5"
FILE_TOO_LARGE = "6"

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
        
def send_sms(receiver, msg_body):
    raise NotImplemented()

def response(messages):
    args = {'messages': messages}
    for m in messages:
        m.save()
    return render('msg.html', args)

def encrypt(data):
    _data = des.encrypt(data).encode("hex")
    return _data

def decrypt(data):
    _data = des.decrypt(data.decode("hex"))
    return _data

def handle_uploaded_file(file):
    try:
        _check_filesize(file)
        ext = _get_file_extension(file.name)
        filename = generate_uuid() + ext
        destination = open(settings.MEDIA_ROOT + filename, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return filename
    except ValueError, ex:
        raise ValueError(ex)

def _get_file_extension(name):
    ext = name[name.rindex('.'):]
    if ext not in ['.jpeg','.jpg','.png']:
        raise ValueError(FILE_TYPE_NOT_SUPPORTED)
    return ext.lower()

def _check_filesize(file):
    if file.size > 5200000:
        raise ValueError(FILE_TOO_LARGE)
    