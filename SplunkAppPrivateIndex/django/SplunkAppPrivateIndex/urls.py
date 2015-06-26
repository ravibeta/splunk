from django.conf.urls import patterns, include, url
from splunkdj.utility.views import render_template as render

urlpatterns = patterns('',
    url(r'^home/$', 'SplunkAppPrivateIndex.views.home', name='home'), 
    url(r'^mystores/$', 'SplunkAppPrivateIndex.views.splunk_view', name='splunk'),
    url(r'^mystores/create/$', 'SplunkAppPrivateIndex.views.index_create', name='index'),
    url(r'^mystores/delete/$', 'SplunkAppPrivateIndex.views.index_delete', name='index'),
    url(r'^myroles/$', 'SplunkAppPrivateIndex.views.role_view', name='roles'),
    url(r'^myroles/create/$', 'SplunkAppPrivateIndex.views.role_create', name='role'),
    url(r'^myroles/delete/$', 'SplunkAppPrivateIndex.views.role_delete', name='role'),
    url(r'^ezIndex/$', 'SplunkAppPrivateIndex.views.securedindex_form_process', name='securedindex'),
)
