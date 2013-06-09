from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('explorer.views',
    url(r'^folder/$', 'folder', name='home'),
    url(r'^folder/(?P<relpath>.*)', 'folder', name='folder'),
)
