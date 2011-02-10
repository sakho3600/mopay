import time
from django.shortcuts import render_to_response as render

from app.common import actions
from app.common.models import message

args = {}
def request(request):
    # analyze message body
    # pass to appropraite handler
    msg = request.GET.get('msg')
    sender = request.GET.get('sender')
    
    msg = msg.lower()
    # log incoming messages
    incoming_msg = {'sender': sender, 'body': msg, 'date': time.time()}
    message.msg_in_save(incoming_msg)
    
    tokens = msg.split(' ')
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