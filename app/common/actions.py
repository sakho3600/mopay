import uuid
import time

from app.common import util
from app.common.models import agent
from app.common.models import card
from app.common.models import transaction
from app.common.models import db
from app.common.models import cashout

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
    receiver = tokens[2]
    
    result = card.get(pin)
    # check if the card is in transaction
    _transaction  = transaction.get_by_pin(pin)
    
    if _transaction: 
        msg = ("This card has already been sent to %s."
                "To cancel, Reply this message with 'cancel'." 
                % _transaction.get('receiver'))
        sms = {'receiver': sender, 'body': msg, 'tid': _transaction.get('id'),
                'type': 'already_sent', 'date': time.time()}
        
        # if sender is not same as the new sender.
        # means card was used by previous sender
        if _transaction.get('sender') != sender:
            msg = "This card has already been used. Thank you for using mopay"
            sms = {'receiver': sender, 'body': msg, 'type': 'already_used',
                 'date': time.time()}
        
        messages.append(sms)
        return util.response(messages)
    
    if result:
        # put into transactions
        _transaction = {'id': str(uuid.uuid4())[:18], 'pin': pin,
                 'sender': sender, 'receiver': receiver,
                 'date': time.time(), 'status': 'active' }
        transaction.save(_transaction)
        
        # build sms for the receiver
        msg = ("%sN  has been sent to you from %s. TransactionId: %s." 
               " Please go to the nearest mopay agent to retrieve." % 
                (result.get('value'), sender, _transaction.get('id')))
        sms = {'receiver': receiver, 'body': msg, 'type': 'notif_receiver',
               'date': time.time(), 'tid': _transaction.get('id')} 
        messages.append(sms)
        
        # build sms for the sender
        msg = ("You have sent %sNGN to %s."
                " TransactionId: %s. Reply this msg with 'cancel' to cancel."
                " Thank you for using mopay."
                % (result.get('value'), receiver, _transaction.get('id')))
        sms = {'receiver': sender, 'body': msg, 'type': 'notif_sender',
               'date': time.time(), 'tid': _transaction.get('id')}
        messages.append(sms)
        
    else:
        # card does not exist
        msg = ("The card you tried to send does not exists. "
               " Card PIN: %s. Thank you for using mopay"
                % pin)
        sms = {'receiver': sender, 'body': msg, 'type': 'invalid_card_pin',
               'date': time.time()}
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
    
    result = db.query('select * from msg_out where receiver=%s and date>%s and \
                     (type=%s or type=%s) order by date DESC limit 0, 1', 
                     (sender, min_time, 'notif_sender', 'already_sent'))
    
    if result:
        _transaction = transaction.get_active_transaction(result.get('tid'))
        if _transaction:
            _transaction['status'] = 'cancelled'
            transaction.update(_transaction)
            
            # build sms for the phone that cancelled the transaction
            msg = ("Transaction with Id: %s has been cancelled." % 
                   _transaction.get('id'))
            sms = {'receiver': sender, 'body': msg, 
                   'type': 'transaction_cancel_sender','date': time.time()} 
            messages.append(sms)
            
            # build sms for the receiver of the transaction
            msg = ("Transaction with Id: %s has been cancelled." % 
                   _transaction.get('id'))
            sms = {'receiver': _transaction.get('receiver'), 'body': msg, 
                   'type': 'transaction_cancel_receiver', 'date': time.time()} 
            messages.append(sms)
            
            return util.response(messages)
    
    msg = "You do not have any active transactions" 
    sms = {'receiver': sender, 'body': msg, 
           'type': 'inactive_transactions', 'date': time.time()}
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
    
    # confirm this guy is an agent
    _agent = agent.get_by_phone(sender)
    if not _agent:
        msg = ("You are not a registered agent. Mopay Inc")
        sms = {'receiver': sender, 'body': msg, 
               'type': 'not_agent','date': time.time()} 
        messages.append(sms)
        return util.response(messages)
    
    _transaction_id = tokens[1]
    
    # confirm this is a valid transaction
    _transaction = transaction.get(_transaction_id)
    if not _transaction:
        msg = "This is not a valid transaction id. Please try again"
        sms = {'receiver': sender, 'body': msg, 
               'type': 'cashout_invalid_transaction_id','date': time.time()} 
        messages.append(sms)
        return util.response(messages)
    
    # got here?? then u are valid
    # send sms to receiver that money is about to be cashed out
    
    # create cashout entity
    _cashout = {'id': util.generate_uuid(), 'agent': sender, 
                'tid': _transaction.get('id'), 
                'receiver': _transaction.get('receiver')}
    cashout.save(_cashout)
    
    msg = ("Your transaction is about to be claimed. Please confirm you are "
           "the one making this claim by replying this message with 'confirm'"
           " within 15mins. Mopay Inc.")
    sms = {'receiver': _transaction.get('receiver'), 'body': msg, 
           'type': 'receiver_confirm_cashout', 'date': time.time(),
           'tid': _transaction.get('id'), 'cashout_id':_cashout.get('id')}
    messages.append(sms)
    
    # build msg to be sent to agent
    msg = ("Your request to cashout transaction: %s has been processed. "
           "Now waiting for receiver confirmation." % (_transaction.get('id')))
    sms = {'receiver': sender, 'body': msg, 
           'type':'cashout_request_in_process', 'date': time.time()}
    messages.append(sms)
    return util.response(messages)

def confirm_cashout(tokens, sender):
    """
    User confirms cashout
    """
    messages = []
    
    diff = time.time() - 900
    
    # get last msg sent to user about a cashout
    _msg = db.query(("select * from msg_out where type=%s and receiver=%s and date > %s order by date desc limit 0, 1"),
                   ('receiver_confirm_cashout', sender, diff))
    if not _msg:
        msg = ("No active cashout requests to confirm. Mopay Inc.")
        sms = {'receiver': sender, 'body': msg, 
                'type':'no_active_cashout_request', 'date': time.time()}
        messages.append(sms)
        return util.response(messages)
    
    # get cashout object that was requested in the last 15 mins.
    
    _cashout = db.query(("select * from cashout where id=%s and date>%s and confirmed=%s"),
                        (_msg.get('cashout_id'), diff, "0"))
    if not _cashout:
        msg = ("The cash out request is no longer active. Mopay Inc.")
        sms = {'receiver': sender, 'body': msg, 
                'type':'cashout_request_expired', 'date': time.time()}
        messages.append(sms)
        return util.response(messages)
    
    # cashout request still on form
    # process can now be completed
    cashout.confirm(_cashout)
    
    _transaction = transaction.get(_msg.get('tid'))
    _transaction['status'] = 'completed'
    
    transaction.update(_transaction)
    
    _card = card.get(_transaction.get('pin'))
    
    # mark card as used
    card.mark_used(_card)
    # build msg to be sent to receiver
    msg = ("Your request to cashout transaction: %s has been confirmed. "
           "Please collect total cash of NGN%s from the agent. Mopay Inc" 
           % (_transaction.get('id'), _card.get('value')))
    sms = {'receiver': sender, 'body': msg, 
           'type':'receiver_cashout_confirmed', 'date': time.time()}
    messages.append(sms)
    
    # build msg to be sent to agent
    msg = ("The request to cashout transaction: %s has been confirmed. "
           "Please pay the customer total cash of NGN%s. Mopay Inc" 
           % (_transaction.get('id'), _card.get('value')))
    sms = {'receiver': _cashout.get('agent'), 'body': msg, 
           'type':'sender_cashout_confirmed', 'date': time.time()}
    messages.append(sms)
    
    #build msg to be sent to the original sender of the cash
    msg = ("%s has just received NGN%s sent by you. Thank you for using Mopay."
           " Mopay Inc" % (_transaction.get('receiver'), _card.get('value')))
    sms = {'receiver': _transaction.get('sender'), 'body': msg, 
           'type':'sender_cashout_confirmed', 'date': time.time()}
    messages.append(sms)
    return util.response(messages)