from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Login/logout, password changes and resets
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='logout'),
    url(r'^password/change/$', 'password_change',
        name='password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        name='password_change_done'),
    url(r'^password/reset/$', 'password_reset',
        name='password_reset'),
    url(r'^password/reset/done/$', 'password_reset_done',
        name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        'password_reset_complete',
        name='password_reset_complete'),
)

# Fallthrough for CMS managed pages
urlpatterns += patterns('',
    url(r'^', include('cms.urls'))
)
