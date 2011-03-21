import hashlib
import time

#from django.db.models import Q
from django.shortcuts import render_to_response as render

import util
from models import OutgoingMessage
#from models import Transaction
#from models import Card
from models import User
#from models import Cashout

def register(tokens, sender_number):
    """
    Complete user registration.
    Expected msg format: 'register [new pin] [new pin]'
    """
    messages = []
    
    new_pin = tokens[1]
    new_pin_confirm = tokens[2]
    
    if new_pin != new_pin_confirm:
        msg = "the pins entered are not the same. please try again"
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
    try:
        user = User.objects.get(phone=sender_number)
        user.pin_salt = util.generate_uuid()
        user.pin = hashlib.md5(new_pin + user.pin_salt).hexdigest()
        user.save()
        
        msg = ("Your registration has been completed. Send '[balance] [pin]' to"
               " check your available balance.")
        sms = OutgoingMessage(body=msg, receiver=user.phone,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    
def balance(tokens, sender_number):
    """
    Return available balance for a user
    Expected message format: 'balance [pin]'
    """
    messages = []

    try:
        pin = tokens[1]
        user = User.objects.get(phone=sender_number)
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        msg = ("Your current account balance is NGN%s . Thank you for"
               " using Mopay." % user.balance)
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        msg = ("Unknow message format. Expected format. 'balance [pin]'")
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
    
def change_pin(tokens, sender_number):
    """
    Change user pin number
    Expected message format: 'change pin [old pin] [new pin] [new pin]'
    """
    messages = []
    try:
        old_pin = tokens[2]
        new_pin = tokens[3]
        new_pin_confirm = tokens[4]
        user = User.objects.get(phone=sender_number)
        
        if not validate_pin(user, old_pin):
            return msg_invalid_pin(user.phone)
        
        if new_pin != new_pin_confirm:
            msg = ("The pin entered are not the same. please try again."
                   " Format: 'change pin [old pin] [new pin] [new pin]'")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time())
            messages.append(sms)
            return send_sms(messages)
        
        user.pin_salt = util.generate_uuid()
        user.pin = hashlib.md5(new_pin + user.pin_salt).hexdigest()
        user.save()
        
        msg = ("Your pin has been successfully changed.")
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
        
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        msg = ("Unknow message format. Expected format. 'change pin" 
               "[old pin] [new pin] [new pin]'")
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
def transaction_history(tokens, sender_number):
    """
    Returns 5 last transactions of the user
    Expected format: 'transaction history [pin]'
    """
    return None

def transfer_funds(tokens, sender_number):
    """
    Transfer funds to user or non-user
    Expected format: 'transfer [amount] [receiver] [pin]'
    
    transaction limit: NGN3,000
    daily transaction limit: NGN30,000
    """
    return None

def load_account(tokens, sender_number):
    """
    Load a user account
    Expected format: 'reload [scratch-card pin] [pin]'
    """
    return None

def cashout(tokens, sender_number):
    """
    Generate cashout ticket
    Expected Format: 'cashout [amount] [pin]'
    """
    return None
    
def send_sms(messages, use_render=True):
    args = {'messages': messages}
    for m in messages:
        m.save()
    if use_render == True:
        return render('admin/msg.html', args)
    
def validate_pin(user, pin):
    if hashlib.md5(pin + user.pin_salt).hexdigest() == user.pin:
        return True
    
def msg_invalid_pin(receiver):
    messages = []
    msg = "Invalid pin number. Please try again"
    sms = OutgoingMessage(body=msg, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return send_sms(messages)

def msg_user_does_not_exist(receiver):
    messages= []
    msg = "Please go to the nearest agent to register."
    sms = OutgoingMessage(body=msg, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return send_sms(messages)

"""
def build_msg(msg_body, receiver, meta=None):
    sms = OutgoingMessage(body=msg_body, receiver=receiver,
                          timestamp=time.time())
    
    if meta:
        sms.meta = meta
        
    messages = [sms]
    send_sms(messages)
"""