import hashlib
import time
from django.shortcuts import render_to_response as render
from django.shortcuts import HttpResponseRedirect as redirect

from app.models import Agent
from app.models import User
from app.models import OutgoingMessage
from app import util
from app import actions

INVALID_LOGIN = "1"
LOGOUT_SUCCESS = "2"
PASSWORD_CHANGED = "3"
PASSWORD_MATCH_FAILED = "4"
USER_REG_SUCCESS = "5"

def _get_args(request):
    args = {'agent': request.session.get('agent'), 'page_name': ''}
    return args
    
def main(request):
    return redirect('/agent/register/user')

def login(request):
    args = _get_args(request)

    if request.GET.get('msg') == INVALID_LOGIN:
        args['msg_error'] = 'Invalid login credentials'
    elif request.GET.get('msg') == LOGOUT_SUCCESS:
        args['msg'] = 'You have successfully logged out'
    
    return render('agent/login.html', args)
    
def login_process(request):
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
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == PASSWORD_MATCH_FAILED:
        args['msg_error'] = 'The passwords dont match'
        
    return render('agent/change_password.html', args)

def change_password_process(request):
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
    args = _get_args(request)
    args['page_name'] = 'register_user'
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == PASSWORD_CHANGED:
        args['msg'] = 'Your password change has been successful'
    elif request.GET.get('msg') == USER_REG_SUCCESS:
        args['msg'] = 'User registration has been completed'
        
    return render('agent/register_user.html', args)

def register_user_process(request):
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.POST.get('form_name') == 'register_user':
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
    args = {'page_name': 'cashout_ticket'}
    return render('agent/cashout_ticket.html', args)
    
def cashout_history(request):
    args = {'page_name': 'cashout_history'}
    return render('agent/cashout_history.html', args)

def user_logged_in(request):
    if request.session.get('agent'):
        return True

def redirect_login():
    return redirect('/agent/login')

def logout(request):
    if request.session.get('agent'):
        del request.session['agent']
        
    return redirect('/agent/login?msg=2')