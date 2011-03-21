import uuid
import time

from django.db.models import Q
from django.shortcuts import render_to_response as render

import util
from models import OutgoingMessage
from models import Transaction
from models import Card
from models import User
#from models import Cashout

def send(tokens, sender):
    """
    Sends A card to a phone number
        format: send card_pin receiver
        
        Before sending the card, we perform few checks.
            we verify the existence of the card.
            Check if the card has already been sent before.
        Then start a new transaction and send notification sms
        to both the sender and receiver
        
    Parameters:
        tokens: the splitted message
        sender: the sender of the message
    """
    messages = []
    
    # check if pin exists
    pin = tokens[1].lower()
    receiver_number = tokens[2]
    
    try:
        receiver = User.objects.get(phone=receiver_number)
    except User.DoesNotExist:
        receiver = User(phone=receiver_number)
        receiver.save()
    
    try:
        card = Card.objects.get(pin=pin)
        try:
            transaction = Transaction.objects.get(Q(card=card), Q(status='active'))
            msg = ("This card has already been sent to %s."
                    "To cancel, Reply this message with 'cancel'." 
                    % transaction.receiver.phone)
            sms = OutgoingMessage(receiver=sender, body=msg, 
                                  transaction=transaction, type='already_sent',
                                  timestamp=time.time())
            if transaction.sender != sender:
                msg = "This card has already been used. Thank you for using mopay"
                sms = OutgoingMessage(receiver=sender, body=msg, 
                                      type='already_used', timestamp=time.time())
                
            messages.append(sms)
            return util.response(messages)
        
        except Transaction.DoesNotExist:
            transaction = Transaction(id=str(uuid.uuid4())[:18], card=card,
                                      sender=sender, receiver=receiver, 
                                      timestamp=time.time(), status='active')
            transaction.save()
            
            # build sms for the receiver
            msg = ("%sN  has been sent to you from %s. TransactionId: %s." 
                   " Please go to the nearest mopay agent to retrieve." % 
                    (card.value, sender, transaction.id))
            sms = OutgoingMessage(receiver=receiver, body=msg, 
                                  type='notif_receiver', timestamp=time.time(),
                                  transaction=transaction)
            messages.append(sms)
            
            # build sms for the sender
            msg = ("You have sent %sNGN to %s."
                    " TransactionId: %s. Reply this msg with 'cancel' to cancel."
                    " Thank you for using mopay."
                    % (card.value, receiver, transaction.id))
            
            sms = OutgoingMessage(receiver=sender, body=msg, 
                                  type='notif_sender', timestamp=time.time(),
                                  transaction=transaction)
            
            messages.append(sms)
            return util.response(messages)
        
    except Card.DoesNotExist:
        msg = ("The card you tried to send does not exists. "
               "Pin sent: %s. Thank you for using mopay"
                % pin)
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='invalid_card_pin', 
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)


def cancel(tokens, sender):
    """
    Cancel an active transaction
    
    A transaction is defined active if there has been activity against it
    in the last 900 seconds. 
    
    The transaction to cancel is determined by checking the last outgoing
    message to the user from the outgoing message log.
    
    The logs that have meta of type in ['notif_sender', 'already_sent']
    fit the profile of sequence for cancelling an active transaction
    
    Parameters:
        tokens: the splitted message
        sender: the sender of the message
    """
    messages = []
    min_time = time.time() - 900
    
    """
    message = OutgoingMessage.objects.filter(receiver=sender) \
                .filter(timestamp__gt=min_time) \
                .filter(type__in=['notif_sender','already_sent']) \
                .order_by('-timestamp')[0]
    """
    try:
        message = OutgoingMessage.objects \
                .filter(Q(receiver=sender), Q(timestamp__gt=min_time),
                        Q(type='notif_sender') | Q(type='already_sent')) \
                .order_by('-timestamp')[0]
                
        Transaction.objects.filter(pk=message.transaction.pk) \
            .update(status='cancelled')
            
        # build sms for the phone that cancelled the transaction
        msg = ("Transaction with Id: %s has been cancelled." % 
               message.transaction.id)
        sms = OutgoingMessage(receiver=sender, body=msg, 
                              type='transaction_cancel_sender', 
                              timestamp=time.time())
        messages.append(sms)
        
        # build sms for the receiver of the transaction
        msg = ("Transaction with Id: %s has been cancelled." % 
               message.transaction.id)
        sms = OutgoingMessage(receiver=message.transaction.receiver, body=msg,
                              type='transaction_cancel_receiver', 
                              timestamp=time.time())
        
        messages.append(sms)
        return util.response(messages)
    except IndexError:
        msg = "You do not have any active transactions"
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='inactive_transaction', 
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)
        
        
def agent_cashout(tokens, sender):
    """
    Cashout command is usally performed by an agent
    
    An sms is sent to the receiver asking user to confirm
    cashout by agent
    
    'cashout transaction-id'
    """
    messages = []
    _transaction_id = tokens[1]
    
    try:
        if sender.is_agent == False:
            
            raise User.DoesNotExist
        transaction = Transaction.objects.get(id=_transaction_id)
    except User.DoesNotExist:
        msg = ("You are not a registered agent. Mopay Inc")
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='not_agent',timestamp=time.time())
        messages.append(sms)
        return util.response(messages)
    except Transaction.DoesNotExist:
        msg = "This is not a valid transaction id. Please try again"
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='cashout_invalid_transaction_id',
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)
    
    cashout = Cashout(id=util.generate_uuid(), agent=sender,
                      transaction=transaction,receiver=transaction.receiver,
                      timestamp=time.time())
    cashout.save()
    
    #build msg for receiver
    msg = ("Your transaction is about to be claimed. Please confirm you are "
           "the one making this claim by replying this message with 'confirm'"
           " within 15mins. Mopay Inc.")
    sms = OutgoingMessage(receiver=transaction.receiver, body=msg,
                          type='receiver_confirm_cashout', timestamp=time.time(),
                          transaction=transaction, cashout=cashout)
    messages.append(sms)
    
    # build msg to be sent to agent
    msg = ("Your request to cashout transaction: %s has been processed. "
           "Now waiting for receiver confirmation." % transaction.id)
    sms = OutgoingMessage(receiver=sender, body=msg,
                          type='cashout_request_processed', 
                          timestamp=time.time())
    messages.append(sms)
    return util.response(messages)


def confirm_cashout(tokens, sender):
    """
    User confirms cashout
    """
    messages = []
    diff = time.time() - 900
    
    # get last msg sent to user about cashout
    try:
        message = OutgoingMessage.objects \
                .filter(Q(type='receiver_confirm_cashout'),
                        Q(receiver=sender),Q(timestamp__gt=diff)) \
                .order_by('-timestamp')[0]
        cashout = Cashout.objects.get(Q(id=message.cashout.id),
                                      Q(timestamp__gt=diff), Q(confirmed=False))
        
        Cashout.objects.filter(pk=cashout.pk).update(confirmed=True)
        Transaction.objects.filter(pk=message.transaction.pk). \
            update(status='completed')
        Card.objects.filter(pk=message.transaction.card.pk). \
            update(used=True)
            
        # build msg to be sent to receiver
        msg = ("Your request to cashout transaction: %s has been confirmed. "
               "Please collect total cash of NGN%s from the agent. Mopay Inc" 
               % (message.transaction.id, message.transaction.card.value))
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='receiver_cashout_confirmed', 
                              timestamp=time.time())
        messages.append(sms)
        
        # build msg to be sent to agent
        msg = ("The request to cashout transaction: %s has been confirmed. "
               "Please pay the customer total cash of NGN%s. Mopay Inc" 
               % (message.transaction.id, message.transaction.card.value))
        sms = OutgoingMessage(receiver=cashout.agent, body=msg,
                              type='agent_cashout_confirmed', 
                              timestamp=time.time())
        messages.append(sms)
        
        #build msg to be sent to the original sender of the cash
        msg = ("%s has just received NGN%s sent by you. Thank you for using Mopay."
               " Mopay Inc" % (message.transaction.receiver, message.transaction.card.value))
        sms = OutgoingMessage(receiver=message.transaction.sender,body=msg,
                              type='sender_cashout_confirmed',
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)
            
    except IndexError:
        msg = ("No active cashout requests to confirm. Mopay Inc.")
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='no_active_cashout_request',
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)
    
    except Cashout.DoesNotExist:
        msg = ("The cash out request is no longer active. Mopay Inc.")
        sms = OutgoingMessage(receiver=sender, body=msg,
                              type='cashout_request_expired', 
                              timestamp=time.time())
        messages.append(sms)
        return util.response(messages)

def send_sms(messages, use_render=True):
    args = {'messages': messages}
    for m in messages:
        m.save()
    if use_render == True:
        return render('msg.html', args)