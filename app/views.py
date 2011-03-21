import time
from django.shortcuts import render_to_response as render

import actions
import util
from models import User
from models import IncomingMessage
from models import OutgoingMessage

args = {}
def request(request):
    # analyze message body
    # pass to appropraite handler
    msg_body = request.GET.get('msg')
    sender_number = request.GET.get('sender')
    
    msg_body = msg_body.lower()
    message = IncomingMessage(sender=sender_number, body=msg_body, 
                                     timestamp=time.time())
    message.save()
    
    try:
        tokens = msg_body.split(' ')
        command = tokens[0]
        """
        if command == 'send':
            return actions.send(tokens, sender)
        elif command == 'cancel':
            return actions.cancel(tokens, sender)
        elif command == 'cashout':
            return actions.agent_cashout(tokens, sender)
        elif command == 'confirm':
            return actions.confirm_cashout(tokens, sender)
        else:
            args = {'error_msg': 'Unknown service command. Please try again' }
            return render('msg.html', args)
        """
        
        if command == 'register':
            return actions.register(tokens, sender_number)
        elif command == 'balance':
            return actions.balance(tokens, sender_number)
        elif command == 'change' and tokens[1] == 'pin':
            return actions.change_pin(tokens, sender_number)
        else:
            return unknown_service_command(sender_number)
    except IndexError:
        return unknown_service_command(sender_number)
    
def unknown_service_command(receiver):
    messages = []
    msg = ("Unknow service command. Reply this message with help.")
    sms = OutgoingMessage(body=msg, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return actions.send_sms(messages)