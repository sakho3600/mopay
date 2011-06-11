import hashlib
import time
from django.shortcuts import render_to_response as render
from django.shortcuts import HttpResponseRedirect as redirect
from django.db.models  import Q

from app.models import Agent
from app.models import User
from app.models import OutgoingMessage
from app.models import CashoutTicket
from app.models import RequestCashoutTicket
from app import util
from app import actions

import settings

INVALID_LOGIN = "1"
LOGOUT_SUCCESS = "2"
PASSWORD_CHANGED = "3"
PASSWORD_MATCH_FAILED = "4"
USER_REG_SUCCESS = "5"

USER_ALREADY_REGISTERED = "7"
FIELDS_EMPTY = "8"

CASHOUT_REQUEST_SUCCESS  = "9"
CASHOUT_REQUEST_ALREADY_SENT = "10"
CASHOUT_ALREADY_MADE = "11"

def _get_args(request):
    """
    Generic args passed to every template
    """
    args = {'agent': request.session.get('agent'), 'page_name': '', 
            'MEDIA_URL': settings.MEDIA_URL}
    return args
    
def main(request):
    return redirect('/agent/register/user')

def login(request):
    """
    Login page for agents
    """
    args = _get_args(request)

    if request.GET.get('msg') == INVALID_LOGIN:
        args['msg_error'] = 'Invalid login credentials'
    elif request.GET.get('msg') == LOGOUT_SUCCESS:
        args['msg'] = 'You have successfully logged out'
    
    return render('agent/login.html', args)
    
def login_process(request):
    """
    Process login forms for agents
    """
    if request.POST.get('form_name') == 'agent_login':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            agent = Agent.objects.get(username=username)
            if hashlib.md5(password + agent.password_salt).hexdigest() == \
                agent.password:
                
                request.session['agent'] = agent
                if password == 'default':
                    return redirect('/agent/change_password')
                
                return redirect('/agent')
            else:
                raise Agent.DoesNotExist('Invalid login credentials')
        except Agent.DoesNotExist:
            return redirect('/agent/login?msg=1')

def change_password(request):
    """
    Change password page for agents.
    """
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == PASSWORD_MATCH_FAILED:
        args['msg_error'] = 'The passwords dont match'
        
    return render('agent/change_password.html', args)

def change_password_process(request):
    """
    Process change_password page
    """
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.POST.get('form_name') == 'change_password':
        new_password = request.POST.get('password')
        confirm_new_password = request.POST.get('confirm_password')
        
        if new_password == confirm_new_password:
            agent = request.session.get('agent')
            password_salt = util.generate_uuid()
            password = hashlib.md5( new_password + password_salt) \
                                .hexdigest()
                                
            Agent.objects.filter(pk=agent.pk) \
                .update(password_salt=password_salt, password=password)
                
            return redirect('/agent/register/user?msg=3')
        
        else:
            return redirect('/agent/change_password?msg=4')
        
def register_user(request):
    """
    Register user page.
        User registration is carried out by agents
    """
    args = _get_args(request)
    args['page_name'] = 'register_user'
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == PASSWORD_CHANGED:
        args['msg'] = 'Your password change has been successful'
    elif request.GET.get('msg') == USER_REG_SUCCESS:
        args['msg'] = 'User registration has been completed'
    elif request.GET.get('msg') == USER_ALREADY_REGISTERED:
        args['msg_error'] = 'The phone number has already been registered'
    elif request.GET.get('msg') == FIELDS_EMPTY:
        args['msg_error'] = "One or more fields are empty. All fields are \
                              compulsory."
    return render('agent/register_user.html', args)

def register_user_process(request):
    """
    Process user registration
    """
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()

    #check if form any field is empty
    __phone = request.POST.get('phone')
    __firstname = request.POST.get('firstname')
    __lastname = request.POST.get('lastname')
    __address = request.POST.get('address')

    if __phone == '' or __firstname == '' or \
            __lastname == '' or __address == '':
        return redirect('/agent/register/user?msg=8')
    
    if request.POST.get('form_name') == 'register_user':
        #check for already existing user
        try:
            _user = User.objects.get(phone=request.POST.get('phone'))
            if hashlib.md5("0000" + _user.pin_salt).hexdigest() == _user.pin:
                #user has not activate his account
                _user.first_name = request.POST.get('firstname')
                _user.last_name = request.POST.get('lastname')
                _user.address = request.POST.get('address')
                _user.phone = request.POST.get('phone')
                # send sms to new user
                msg = ("Please respond to this sms with your new PIN, in the format"
                       " 'register [new pin] [new pin]' to complete the registration.")
                sms = OutgoingMessage(receiver=_user.phone, body=msg,
                                      timestamp=time.time(), type='user_reg')
                messages = [sms]
                actions.send_sms(messages, use_render=False)
                return redirect('/agent/register/user?msg=5')
            else:
                # this account is already activated
                return redirect('/agent/register/user?msg=7')
        except User.DoesNotExist:
            user = User()
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.address = request.POST.get('address')
            user.phone = request.POST.get('phone')
            
            default_pin = '0000'
            user.pin_salt = util.generate_uuid()
            user.pin = hashlib.md5(default_pin + user.pin_salt).hexdigest()
            
            # send sms to new user
            msg = ("Please respond to this sms with your new PIN, in the format"
                   "'register [new pin] [new pin]' to complete the registration.")
            sms = OutgoingMessage(receiver=user.phone, body=msg,
                                  timestamp=time.time(), type='user_reg')
            messages = [sms]
            actions.send_sms(messages, use_render=False)
            user.save()
            
            return redirect('/agent/register/user?msg=5')

def cashout_ticket(request):
    """
    Cashout ticket page for agent.
    Description: 
        Basically a search box for the agent to search for ticket he
        wants to cashout
    """
    args = _get_args(request)
    args['page_name'] = 'cashout_ticket'
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('q'):
        try:
            q = request.GET.get('q')
            cashout_ticket = CashoutTicket.objects.get(Q(id=q))
            
            return redirect('/agent/cashout/ticket/details?ticket=%s' % cashout_ticket.id)
        except CashoutTicket.DoesNotExist:
            args['msg_error'] = 'The ticket was not found. Please try again'
    
    return render('agent/cashout_ticket.html', args)

def cashout_ticket_details(request):
    """
    Details page for a ticket that an agent wants to cashout
    """
    args = _get_args(request)
    args['page_name'] = 'cashout_ticket'
    
    min_time = time.time() - 900
    if not user_logged_in(request):
        return redirect_login()
    
    if not request.GET.get('ticket'):
        return redirect('/agent/cashout/ticket')
    
    if request.GET.get('msg') == CASHOUT_REQUEST_SUCCESS:
        args['msg'] = ("Cashout Request is successful. Please pay the customer.")

    elif request.GET.get('msg') == CASHOUT_REQUEST_ALREADY_SENT:
        args['msg_error'] = ("Cashout request has already been sent to the "
                             "receiver. Please wait for confirmation.")
    elif request.GET.get('msg') == CASHOUT_ALREADY_MADE:
        args['msg_error'] = ("Cashout has already been made on this ticket.")
        
    try:
        ticket_id = request.GET.get('ticket')
        ticket = CashoutTicket.objects.get(Q(id=ticket_id))
        
        args['ticket'] = ticket
        args['request_cashout_tickets'] = RequestCashoutTicket.\
            objects.filter(Q(cashout_ticket=ticket),
                           Q(timestamp__gt=min_time) | Q(confirmed=True)).order_by('-timestamp')
        
        request_cashout_tickets = [x for x in args['request_cashout_tickets']]
        if len(request_cashout_tickets) == 0:
            args['request_cashout_tickets'] = None
                           
        return render('agent/cashout_ticket_details.html', args)
        
    except CashoutTicket.DoesNotExist:
        return redirect('/agent/cashout/ticket') 

"""    
def cashout_ticket_details_process(request):

        Simply process the cashout for a ticket from 
        cashout_ticket_details page

    messages = []
    args = _get_args(request)
    
    min_time = time.time() - 900
    if request.POST.get('form_name') == 'request_ticket_cashout':
        ticket_id = request.POST.get('ticket_id')
        cashout_ticket = CashoutTicket.objects.get(Q(id=ticket_id))
        
        try:
            request_cashout_ticket = RequestCashoutTicket. \
                objects.get(Q(cashout_ticket=cashout_ticket), 
                            Q(timestamp__gt=min_time))
            
            if request_cashout_ticket.confirmed == True:
                msg = CASHOUT_ALREADY_MADE
            else:
                msg = CASHOUT_REQUEST_ALREADY_SENT
            
        except RequestCashoutTicket.DoesNotExist: 
            request_cashout_ticket = RequestCashoutTicket(
                agent=args['agent'], cashout_ticket=cashout_ticket,
                timestamp=time.time())
            request_cashout_ticket.save()
        
            # send mesage to receiver to confirm cashout
            msg = ("You are requesting cashout from an agent on ticket: %s. "
                   "Please to confirm, reply this message with 'confirm'")
            sms = OutgoingMessage(body=msg, receiver=cashout_ticket.receiver,
                                  timestamp=time.time(), type="confirm_cashout",
                                  meta=request_cashout_ticket)
            messages.append(sms)
            actions.send_sms(messages, use_render=False)
            
            msg = CASHOUT_REQUEST_SENT
        
        return redirect('/agent/cashout/ticket/details?ticket=%s&msg=%s'
                        % (ticket_id, msg))
"""

def cashout_ticket_details_process(request):
    messages = []
    args = _get_args(request)
   
    if request.POST.get('form_name') == 'request_ticket_cashout':
        ticket_id = request.POST.get('ticket_id')
        cashout_ticket = CashoutTicket.objects.get(Q(id=ticket_id))

        try:
            request_cashout_ticket = RequestCashoutTicket. \
                objects.get(Q(cashout_ticket=cashout_ticket))

            if request_cashout_ticket.confirmed:
                msg = CASHOUT_ALREADY_MADE
            
        except RequestCashoutTicket.DoesNotExist:
            request_cashout_ticket = RequestCashoutTicket(
                agent=args['agent'], cashout_ticket=cashout_ticket,
                timestamp=time.time(), confirmed=True)
            request_cashout_ticket.save()
            
            msg = CASHOUT_REQUEST_SUCCESS

        return redirect('/agent/cashout/ticket/details?ticket=%s&msg=%s'
                            % (ticket_id, msg))
                
def cashout_history(request):
    args = _get_args(request)
    args['page_name'] = 'cashout_history'
    
    request_cashouts = RequestCashoutTicket.objects. \
        filter(Q(agent=args['agent']), Q(confirmed=True)).order_by('-timestamp')
    
    args['request_cashouts'] = request_cashouts
    
    return render('agent/cashout_history.html', args)

def cashout_active_requests(request):
    args = _get_args(request)
    args['page_name'] = 'cashout_active_requests'
    
    min_time = time.time() - 1800
    request_cashouts = RequestCashoutTicket.objects. \
        filter(Q(agent=args['agent']), Q(timestamp__gt=min_time)).order_by('-timestamp')
        
    request_cashouts = [x for x in request_cashouts]
    if len(request_cashouts) == 0:
        args['msg'] = 'There are no active cashout requests.'
        
    args['request_cashouts'] = request_cashouts
    
    return render('agent/cashout_active_requests.html', args)

def user_logged_in(request):
    """
    Simple function to make sure a user is logged in
    """
    if request.session.get('agent'):
        return True

def redirect_login():
    """
    Redirect to login page
    """
    return redirect('/agent/login')

def logout(request):
    """
    Logout an agent from the application.
    """
    if request.session.get('agent'):
        del request.session['agent']
        
    return redirect('/agent/login?msg=2')
