import hashlib
import time
import datetime
from django.shortcuts import render_to_response as render
from django.shortcuts import HttpResponseRedirect as redirect

from app.models import User
from app.models import Admin
from app.models import Agent
from app.models import OutgoingMessage
from app import util

INVALID_LOGIN = "1"
LOGOUT_SUCCESS = "2"

FILE_TYPE_NOT_SUPPORTED = "5"
FILE_TOO_LARGE = "6"

args = {}

def _get_args(request):
    args = {'admin': request.session.get('admin')}
    return args

def main(request):
    return redirect('/admin/manage/users')

def play(request):
    args['page_name'] = 'play'
    args['password'] = 'password'
    args['password_salt'] = 'fx123ddsf09568#$@!'
    args['password_hash'] = hashlib.md5(args['password'] + args['password_salt']).hexdigest()
    """
    msg = OutgoingMessage()
    msg.meta = datetime.datetime.now()
    msg.body = "play"
    msg.receiver = User.objects.get(pk=1)
    msg.timestamp = time.time()
    msg.save()
    """
    """
    msg = OutgoingMessage.objects.get(pk=1)
    args['meta'] = msg.meta
    args['meta_other'] = datetime.datetime.fromtimestamp(float(msg.timestamp))
    """
    return render('admin/play.html', args)

def cards(request):
    """Admin Cards Page"""
    
    args = _get_args(request)
    args['page_name'] = 'cards'
    
    if not user_logged_in(request):
        return redirect_login()
    
    return render('admin/cards.html', args)

def agents(request):
    """ Admin manage agent view 
        url: /admin/manage/agents
    """
    args = _get_args(request)
    args['page_name'] = 'agents'
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == "1":
        args['msg'] = "Agent has been successfully added"
    
    args['agents'] = Agent.objects.all()
    
    return render('admin/agents.html', args)

def agents_add(request):
    """ Admin add agent view 
        url: /admin/manage/agents/add
    """
    args = _get_args(request)
    args['page_name'] = 'agents'
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.GET.get('msg') == FILE_TOO_LARGE:
        args['msg_error'] = "File size is too large"
    elif request.GET.get('msg') == FILE_TYPE_NOT_SUPPORTED:
        args['msg_error'] = "File type not supported"
    
    return render('admin/agents_add.html', args)

def agents_add_process(request):
    """ Admin: Process add agent form"""
    args = _get_args(request)
    
    if not user_logged_in(request):
        return redirect_login()
    
    if request.POST.get('form_name') == 'add_agent':
        agent = Agent()
        agent.first_name = request.POST.get('first_name')
        agent.last_name = request.POST.get('last_name')
        agent.username = request.POST.get('username')
        agent.phone = request.POST.get('phone')
        agent.address = request.POST.get('address')
        
        try:
            agent.id_filename = util.handle_uploaded_file(request.FILES.get('id'))
            agent.sig_filename = util.handle_uploaded_file(request.FILES.get('sig'))
            password = "default"
            agent.password_salt = util.generate_uuid()
            agent.password = hashlib.md5(password + agent.password_salt) \
                                .hexdigest()
            agent.save()
            return redirect('/admin/manage/agents?msg=1')
        except ValueError, ex:
            return redirect('/admin/manage/agents/add?msg=' + str(ex))

def users(request):
    args = _get_args(request)
    args['page_name'] = 'users'
    
    if not user_logged_in(request):
        return redirect_login()
    
    return render('admin/users.html', args)

def transaction_log(request):
    args = _get_args(request)
    args['page_name'] = 'transaction_log'
    
    if not user_logged_in(request):
        return redirect_login()
    
    return render('admin/transaction_log.html', args)

def incoming_message_log(request):
    args = _get_args(request)
    args['page_name'] = 'incoming_message_log'
    
    if not user_logged_in(request):
        return redirect_login()
    
    return render('admin/incoming_message_log.html', args)

def outgoing_message_log(request):
    args = _get_args(request)
    args['page_name'] = 'outgoing_message_log'
    
    if not user_logged_in(request):
        return redirect_login()
    
    return render('admin/outgoing_message_log.html', args)

def random(request):
    args = {'page_name': ''}
    util.generate_cards()
    return render('admin/index.html', args)

def login(request):
    args = _get_args(request)
    
    if request.GET.get('msg') == INVALID_LOGIN:
        args['msg_error'] = 'Invalid admin login credentials'
    elif request.GET.get('msg') == LOGOUT_SUCCESS:
        args['msg'] = 'You have successfully logged out'
        
    return render('admin/login.html', args)

def login_process(request):
    args = {}
    if request.POST.get('form_name') == 'admin_login':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            admin = Admin.objects.get(username=username)
            if hashlib.md5(password + admin.password_salt).hexdigest() == \
                admin.password:
                
                request.session['admin'] = admin
                return redirect('/admin')
            else:
                raise Admin.DoesNotExist('Invalid login credentials')
        except Admin.DoesNotExist:
            return redirect('/admin/login?msg=1')

def logout(request):
    args = {}
    if request.session.get('admin'):
        del request.session['admin']
        
    return redirect('/admin/login?msg=2')

def user_logged_in(request):
    if request.session.get('admin'):
        return True

def redirect_login():
    return redirect('/admin/login')
