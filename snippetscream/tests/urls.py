from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^some/url/$', 'app.views.view'),
    url(r'^some/other/url/$', 'app.views.other.view', name='this_is_a_named_view'),
)
