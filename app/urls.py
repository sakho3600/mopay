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
    
    (r'^request$', 'app.main.views.request'),
    (r'^random$', 'app.main.views.random'),
    (r'^play$', 'app.main.views.play'),
    
    (r'^cards$', 'app.main.views.cards'),
    (r'^agents$', 'app.main.views.agents'),
    (r'^log/transactions$', 'app.main.views.transaction_log'),
    (r'^log/incoming/message$', 'app.main.views.incoming_message_log'),
    (r'^log/outgoing/message$', 'app.main.views.outgoing_message_log'),
    
    (r'^login$', 'app.main.views.login'),
)
