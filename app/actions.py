import hashlib
import time
import MySQLdb as db

from django.db.models import Q
from django.shortcuts import render_to_response as render

import util
from models import OutgoingMessage
from models import Transaction
from models import Card
from models import User
from models import CashoutTicket

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
                              timestamp=time.time(), type='complete_reg')
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
        
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        msg = ("Your current account balance is NGN%s . Thank you for"
               " using Mopay." % user.balance)
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time(), type='user_balance')
        messages.append(sms)
        return send_sms(messages)
    
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unknow message format. Expected format."
                           " 'balance [pin]'")
        return msg_unknown_format(expected_format, sender_number)
    
    
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
        
        
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
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
                              timestamp=time.time(), type='change_pin')
        messages.append(sms)
        return send_sms(messages)
        
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unknow message format. Expected format. 'change pin" 
                           "[old pin] [new pin] [new pin]'")
        return msg_unknown_format(expected_format, sender_number)
    
def transaction_history(tokens, sender_number):
    """
    Returns 5 last transactions of the user
    Expected format: 'transaction history [pin]'
    """
    messages = []
    try:
        pin = tokens[2]
        user = User.objects.get(phone=sender_number)
        
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        transactions = Transaction.objects.filter(
            Q(sender=sender_number) | Q(receiver=sender_number)). \
            order_by('-timestamp')[0:5]
            
        # convert to list
        transactions = [x for x in transactions]
        
        msg = ""
        for x in transactions:
            msg = msg + "tran-id: %s,amount: %s, " % (x.id, x.amount)
            if x.sender == x.receiver:
                msg = msg + "type: cashout"
            elif x.sender == sender_number:
                msg = msg + "to: %s" % (x.receiver)
            elif x.receiver == sender_number:
                msg = msg + "from: %s" % (x.sender)
            
            if transactions.index(x) != (len(transactions) - 1):
                msg = msg + " | "
        
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time(), type='transaction_history')
        messages.append(sms)
        return send_sms(messages)
            
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unknow message format. Expected format. 'transaction" 
                           " history [pin]'")
        return msg_unknown_format(expected_format, sender_number)

def load_account(tokens, sender_number):
    """
    Load a user account
    Expected format: 'reload [scratch-card pin] [pin]'
    """
    messages = []
    try:
        card_pin = tokens[1]
        pin = tokens[2].lower()
        
        user = User.objects.get(phone=sender_number)
        
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        card = Card.objects.get(pin=card_pin)
        if card.used:
            msg = "The card has already been used. Thank you for using mopay."
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time())
            messages.append(sms)
            return send_sms(messages)
        
        else:
            card.used = True
            user.balance = user.balance + card.value
            user.save()
            card.save()
            
            msg = ("Your account balance has been successfully loaded. Your"
                   " new balance is %s" % user.balance)
            sms = OutgoingMessage(
                body=msg, receiver=sender_number, timestamp=time.time(), 
                type='load_account_success')
            messages.append(sms)
            return send_sms(messages)
    
    except Card.DoesNotExist:
        msg = "The card you have entered does not exist. Please try again."
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time())
        messages.append(sms)
        return send_sms(messages)
    
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unkown message format. Expected message format:"
                           " 'reload [scratch-card pin] [pin]'")
        return  msg_unknown_format(expected_format, sender_number)

def transfer_funds(tokens, sender_number):
    """
    Transfer funds to user or non-user
    Expected format: 'transfer [amount] [receiver] [pin]'
    
    transaction limit: NGN3,000
    daily transaction limit: NGN30,000
    """
    messages = []
    try:
        amount = float(tokens[1])
        receiver_number = tokens[2]
        pin = tokens[3]
        
        user = User.objects.get(phone=sender_number)
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
        # check account balance
        if amount > (user.balance - 100):
            msg = ("You do not have enough balance to make this transfer.")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time(), 
                                  type='insufficient_balance')
            messages.append(sms)
            return send_sms(messages)
        
        if amount > 3000:
            msg = ("You cannot transfer above NGN3,000 in one transaction."
                   " Please try again.")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time(), type='excess_transfer')
            messages.append(sms)
            return send_sms(messages)
        
        # add restriction of daily limit of 3ok
        
        # validate receiver exists
        #     if not generate cash out ticket instead
        transaction = Transaction(
            id=util.generate_uuid()[0:12], sender=user.phone, 
            receiver=receiver_number, timestamp=time.time(), amount=amount)
        try:
            User.objects.get(phone=receiver_number)
            transaction.type = 'user_to_user_transfer'
        except User.DoesNotExist:
            transaction.type = 'user_to_guest_transfer'
            
        transaction.save()
        
        # return message to confirm transaction
        msg = ("transaction-id: %s, amount: %s, receiver: %s. Please"
               " reply this message with 'confirm' to confirm this"
               " transaction." 
               % (transaction.id, transaction.amount, transaction.receiver))
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time(), meta=transaction,
                              type='confirm_transaction')
        messages.append(sms)
        return send_sms(messages)
        
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unknown message format. Expeted format: transfer"
                           " [amount] [receiver] [pin]. Please try again.")
        return msg_unknown_format(expected_format, sender_number)
    
def confirm(tokens, sender_number):
    """
    Confirming a transaction or a cashout ticket.
    """
    messages = []
    min_time = time.time() - 900
    
    try:
        last_msg = OutgoingMessage.objects. \
            filter(Q(receiver=sender_number)).order_by('-timestamp')[0]
            
        msg_req_confirm = ['confirm_transaction', 'confirm_cashout']
        if last_msg.type not in msg_req_confirm:
            raise ValueError
        
        if last_msg.timestamp < min_time:
            # late response, nuke transaction
            # last_msg.meta.staus = 'expired'
            # last_msg.meta.save()
            
            msg = ("Your transaction has expired because you failed to repond "
                   "in 15mins.")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time())
            messages.append(sms)
            return send_sms(messages)
        
        if last_msg.type == 'confirm_transaction':
            transaction = last_msg.meta
            return confirm_transaction(transaction)
        
        elif last_msg.type == 'confirm_cashout':
            request_cashout = last_msg.meta
            return confirm_cashout(request_cashout)
            
    except ValueError:
        msg = "You do not have any active transactions."
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time(), type='inactive transactions')
        messages.append(sms)
        return send_sms(messages)

def cashout(tokens, sender_number):
    """
    Generate cashout ticket
    Expected Format: 'cashout [amount] [pin]'
    """
    messages = []
    try:
        amount = float(tokens[1])
        pin = tokens[2]
        
        user = User.objects.get(phone=sender_number)
        if not account_activated(user):
            return msg_account_not_activated(user.phone)
        
        if not validate_pin(user, pin):
            return msg_invalid_pin(user.phone)
        
        # check account balance
        if amount > (user.balance - 100):
            msg = ("You do not have enough balance to cashout.")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time(), 
                                  type='insufficient_balance')
            messages.append(sms)
            return send_sms(messages)
        
        if amount > 3000:
            msg = ("You cannot cashout above NGN3,000 in one transaction."
                   " Please try again.")
            sms = OutgoingMessage(body=msg, receiver=sender_number,
                                  timestamp=time.time(), type='excess_cashout')
            messages.append(sms)
            return send_sms(messages)
        
        transaction = Transaction(
            id=util.generate_uuid()[0:12], sender=user.phone, 
                receiver=user.phone, timestamp=time.time(), amount=amount,
                type='user_cashout')
        
        # return message to confirm transaction
        msg = ("transaction-id: %s, amount: %s, type: cashout. Please"
               " reply this message with 'confirm' to confirm this"
               " transaction." % (transaction.id, transaction.amount))
        sms = OutgoingMessage(body=msg, receiver=sender_number,
                              timestamp=time.time(), meta=transaction,
                              type='confirm_transaction')
        messages.append(sms)
        return send_sms(messages)
        
    except User.DoesNotExist:
        return msg_user_does_not_exist(sender_number)
    
    except IndexError:
        expected_format = ("Unkown message format. Expected message format:"
                           " 'cashout [amount] [pin]'")
        return  msg_unknown_format(expected_format, sender_number)
    return None
    
def send_sms(messages, use_render=True):
    args = {'messages': messages}
    #_msg_args = {'action': 'sendMessage', 'ozMsUserInfo':'admin:abc123'}
    #_root_url = "http://192.168.137.1:9501/ozeki?"
    for m in messages:
        
        #_msg_args['recepient'] = m.receiver
        #_msg_args['messageData'] = m.body
        
        #file = urllib2.urlopen(_root_url + urllib.urlencode(_msg_args))
        #file.read()
        ozeki_sms_out(m.receiver, m.body)
        m.save()
        
    if use_render == True:
        return render('admin/msg.html', args)
    
def validate_pin(user, pin):
    if hashlib.md5(pin + user.pin_salt).hexdigest() == user.pin:
        return True
    
def account_activated(user):
    """
    Dirty hack to make sure an account is activated before use
    """
    if hashlib.md5("0000" + user.pin_salt).hexdigest() != user.pin:
        return True

def msg_account_not_activated(receiver):
    messages = []
    msg = ("Your registration has not been completed. Reply with 'register"
           " [new-pin] [new-pin]' to complete registration")
    sms = OutgoingMessage(body=msg, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return send_sms(messages)

    
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

def msg_unknown_format(expected_format, receiver):
    messages = []
    sms = OutgoingMessage(body=expected_format, receiver=receiver,
                          timestamp=time.time())
    messages.append(sms)
    return send_sms(messages)

def confirm_transaction(transaction):
    messages = []
    if transaction.type == 'user_to_user_transfer':
        receiver = User.objects.get(phone=transaction.receiver)
        sender = User.objects.get(phone=transaction.sender)
        
        receiver.balance = receiver.balance + transaction.amount
        sender.balance = sender.balance - transaction.amount
        
        transaction.status = 'complete'
        receiver.save()
        sender.save()
        transaction.save()
        
        # send confirmation to both parties
        # receiver's notification
        msg = ("NGN%s has been successfully transferred from the account "
               " of %s. Your new balance is %s. Thank you for using Mopay."
               % (transaction.amount, transaction.sender, receiver.balance))
        sms = OutgoingMessage(body=msg, receiver=transaction.receiver,
                              timestamp=time.time(), 
                              type='transfer_notif_receiver_completed')
        messages.append(sms)
        
        # sender's notification
        msg = ("You have successfully transferred NGN%s to %s. Your new" 
               "balance is NGN%s Thank you for using Mopay." 
               % (transaction.amount, transaction.receiver, sender.balance))
        sms = OutgoingMessage(body=msg, receiver=transaction.sender, 
                              timestamp=time.time(),
                              type='transfer_notif_sender_completed')
        messages.append(sms)
        return send_sms(messages)
    
    elif transaction.type == 'user_to_guest_transfer':
        sender = User.objects.get(phone=transaction.sender)
        sender.balance = sender.balance - transaction.amount
        
        cashout_ticket = CashoutTicket(
            id=util.generate_uuid()[0:15],sender=sender.phone,
            receiver=transaction.receiver,transaction=transaction,
            timestamp=time.time())
        
        cashout_ticket.save()
        
        transaction.status = 'generated_guest_cashout'
        sender.save()
        transaction.save()
        
        # send notifications
        # receiver's notification.
        msg = ("NGN%s has been sent to you from the account of %s."
               " Ticket-ID: %s. Please go to the nearest mopay agent to"
               " retrieve." 
               % (transaction.amount, transaction.sender, cashout_ticket.id))
        sms = OutgoingMessage(body=msg, receiver=transaction.receiver,
                              timestamp=time.time(),
                              type='notif_receiver_transfer_cashout')
        messages.append(sms)
        
        # sender's notificationDoesNotExist
        msg = ("You have sent NGN%s to %s. Thank you for using mopay."
               % (transaction.amount, transaction.receiver))
        sms = OutgoingMessage(body=msg, receiver=transaction.sender,
                              timestamp=time.time(),
                              type='notif_sender_cashout_gen')
        messages.append(sms)
        return send_sms(messages)
    
    elif transaction.type == 'user_cashout':
        sender = User.objects.get(phone=transaction.sender)
        sender.balance = sender.balance - transaction.amount
        
        cashout_ticket = CashoutTicket(
            id=util.generate_uuid()[0:15],sender=sender.phone,
            receiver=transaction.receiver,transaction=transaction,
            timestamp=time.time())
        
        cashout_ticket.save()
        transaction.status = 'cashout_ticket_generated'
        sender.save()
        transaction.save()
        
        msg = ("NGN%s been deducted from your account for a cashout ticket."
               " Ticket-ID: %s. Please go to the nearest mopay agent to"
               " retrieve." % (transaction.amount, cashout_ticket.id))
        sms = OutgoingMessage(body=msg, receiver=transaction.receiver,
                              timestamp=time.time(),
                              type='notif_receiver_transfer_cashout')
        messages.append(sms)
        return send_sms(messages)
    
    
def confirm_cashout(request_cashout):
    messages = []
    request_cashout.confirmed = True
    request_cashout.save()
    
    # notify receiver to collect from agent.
    msg = ("Your cashout for TICKET: %s has been confirmed. Please collect "
           "NGN%s from the agent. Thank you for using mopay" 
           % (request_cashout.cashout_ticket.id,
              request_cashout.cashout_ticket.transaction.amount))
    sms = OutgoingMessage(body=msg, receiver=request_cashout.cashout_ticket.receiver,
                          timestamp=time.time(),type='notif_receiver_cashout_complete')
    messages.append(sms)
    return send_sms(messages)



def ozeki_sms_out(receiver, body):
    query = "insert into ozekimessageout(receiver, msg) values(%s, %s)"
    args = (receiver, body)
    ozeki_db_query(query, args)
    
def ozeki_db_query(query, args=()):
    con = db.connect(host='localhost', user='dammy', \
                        passwd='dammy', db='ozeki')
    cursor = con.cursor(db.cursors.DictCursor)
    cursor.execute(query, args)
    result = cursor.fetchall()
    if len(result) == 0:
        result = None
    con.commit()
    con.close()
    return result
    
    