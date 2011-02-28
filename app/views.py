import time
from django.shortcuts import render_to_response as render

import models

from common import actions

args = {}
def request(request):
    # analyze message body
    # pass to appropraite handler
    msg_body = request.GET.get('msg')
    sender_number = request.GET.get('sender')
    
    msg_body = msg_body.lower()
    
    try:
        sender = models.User.objects.get(phone=sender_number)
    except models.User.DoesNotExist:
        sender = models.User(phone=sender_number)
        sender.save()
    
    message = models.IncomingMessage(sender=sender, body=msg_body, 
                                     timestamp=time.time())
    message.save()

    tokens = msg_body.split(' ')
    command = tokens[0]
    
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
        
def play(request):
    args = {'page_name': 'play'}
    return render('play.html', args)

def cards(request):
    args['page_name'] = 'cards'
    return render('cards.html', args)

def agents(request):
    args['page_name'] = 'agents'
    return render('agents.html', args)

def transaction_log(request):
    args['page_name'] = 'transaction_log'
    return render('transaction_log.html', args)

def incoming_message_log(request):
    args['page_name'] = 'incoming_message_log'
    return render('incoming_message_log.html', args)

def outgoing_message_log(request):
    args['page_name'] = 'outgoing_message_log'
    return render('outgoing_message_log.html', args)

def login(request):
    return render('login.html', args)