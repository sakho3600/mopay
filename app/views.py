import time
from django.shortcuts import render_to_response as render

import actions
from models import IncomingMessage
from models import OutgoingMessage

args = {}
def request(request):
    # analyze message body
    # pass to appropraite handler
    msg_body = request.GET.get('msg')
    sender_number = request.GET.get('sender')
    
    if sender_number[:4] == '+234':
        sender_number = '0' + sender_number[4:]
    
    msg_body = msg_body.lower()
    message = IncomingMessage(sender=sender_number, body=msg_body, 
                                     timestamp=time.time())
    message.save()
    
    try:
        tokens = msg_body.split(' ')
        command = tokens[0]
        
        if command == 'register':
            return actions.register(tokens, sender_number)
        elif command == 'balance':
            return actions.balance(tokens, sender_number)
        elif command == 'reload':
            return actions.load_account(tokens, sender_number)
        elif command == 'change' and tokens[1] == 'pin':
            return actions.change_pin(tokens, sender_number)
        elif command == 'transfer':
            return actions.transfer_funds(tokens, sender_number)
        elif command == 'cashout':
            return actions.cashout(tokens, sender_number)
        elif command == 'confirm':
            return actions.confirm(tokens, sender_number)
        elif command == 'transaction' and tokens[1] == 'history':
            return actions.transaction_history(tokens, sender_number)
        else:
            return unknown_service_command(sender_number)
        
    except IndexError:
        return unknown_service_command(sender_number)
    
def unknown_service_command(receiver):
    messages = []
    msg = ("Unknow service command. Thank you for using Mopay.")
    sms = OutgoingMessage(body=msg, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return actions.send_sms(messages)