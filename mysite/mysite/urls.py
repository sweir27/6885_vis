from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    url(r'^vis/$', 'vis.views.index'),
    url(r'^api/get_me_the_torrents/$', 'vis.views.get_torrents'),
    url(r'^api/get_me_the_locations/$', 'vis.views.get_locations'),
    # url(r'^api/get_paged_torrents/(?P<lb>\w+)$', 'vis.views.get_paged_torrents'),
    url(r'^api/filter_by_checkboxes/(?P<lb>\w+)/(?P<books>\w+)/(?P<music>\w+)/(?P<movies>\w+)/(?P<tv>\w+)/(?P<pirate>\w+)/(?P<kat>\w+)/(?P<seedpeer>\w+)/$', 'vis.views.get_filtered_torrents'),
    url(r'^api/filter_by_checkboxes/(?P<lb>\w+)/(?P<books>\w+)/(?P<music>\w+)/(?P<movies>\w+)/(?P<tv>\w+)/(?P<pirate>\w+)/(?P<kat>\w+)/(?P<seedpeer>\w+)/(?P<title>.*)/$', 'vis.views.get_titled_torrents')
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

urlpatterns += staticfiles_urlpatterns()