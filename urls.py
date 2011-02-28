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
    
    (r'^cards$', 'app.views.cards'),
    (r'^agents$', 'app.views.agents'),
    (r'^log/transactions$', 'app.views.transaction_log'),
    (r'^log/incoming/message$', 'app.views.incoming_message_log'),
    (r'^log/outgoing/message$', 'app.views.outgoing_message_log'),
    
    (r'^login$', 'app.views.login'),
)
