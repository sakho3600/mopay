from django.conf.urls.defaults import patterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^mopay/', include('mopay.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
    (r'^request$', 'app.views.request'),
    (r'^random$', 'app.views.random'),
    (r'^play$', 'app.views.play'),
    
    # agents center
    (r'^agent$', 'app.agent.views.main'),
    (r'^agent/register/user$', 'app.agent.views.register_user'),
    (r'^agent/register/user/process$', 'app.agent.views.register_user_process'),
    (r'^agent/cashout/ticket$', 'app.agent.views.cashout_ticket'),
    (r'^agent/cashout/history$', 'app.agent.views.cashout_history'),
    
    
    (r'^agent/login$', 'app.agent.views.login'),
    (r'^agent/login_process$', 'app.agent.views.login_process'),
    (r'^agent/logout$', 'app.agent.views.logout'),
    
    (r'^agent/change_password$', 'app.agent.views.change_password'),
    (r'^agent/change_password/process$', 'app.agent.views.change_password_process'),
    
    #admin center
    (r'^admin$', 'app.admin.views.main'),
    
    (r'^admin/log/transactions$', 'app.admin.views.transaction_log'),
    (r'^admin/log/incoming/message$', 'app.admin.views.incoming_message_log'),
    (r'^admin/log/outgoing/message$', 'app.admin.views.outgoing_message_log'),
    
    (r'^admin/manage/users$', 'app.admin.views.users'),
    
    (r'^admin/manage/agents$', 'app.admin.views.agents'),
    (r'^admin/manage/agents/add$', 'app.admin.views.agents_add'),
    (r'^admin/manage/agents/add_process$', 'app.admin.views.agents_add_process'),
    
    (r'^admin/manage/cards$', 'app.admin.views.cards'),
    
    (r'^admin/play$', 'app.admin.views.play'),
    
    (r'^admin/login$', 'app.admin.views.login'),
    (r'^admin/logout$', 'app.admin.views.logout'),
    (r'^admin/login_process$', 'app.admin.views.login_process'),
)
