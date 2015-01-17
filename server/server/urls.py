from django.conf.urls import patterns, include, url
from django.contrib import admin
import mobile.views as views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^addUser', views.addUser),
    # url(r'^updateUserName' ,views.updateUserName),
    # url(r'^getUser', views.getUserByID),
    url(r'^addGroup', views.addGroup),
    # url(r'^getJoinGroup', views.getJoinGroup),
    # url(r'^getOwnGroup', views.getOwnGroup),
    # url(r'^getChoice', views.getChoice),


)
