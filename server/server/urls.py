from django.conf.urls import patterns, include, url
from django.contrib import admin
import mobile.views as views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^addUser', views.addUser),
    url(r'^testpost', views.testFrom),
    # url(r'^updateUserName' ,views.updateUserName),
    url(r'^addChoose',views.addChoose),
    url(r'^viewUser', views.viewUserName),
    url(r'^vote', views.vote),
    url(r'^parseUserID', views.parseUserID),
    url(r'^viewGroup', views.viewGroup),
    url(r'^addGroup', views.addGroup),
    url(r'^join', views.join),
    url(r'^viewMember', views.viewAllUsersInGroup),
    url(r'^viewVoteMember', views.viewVoteMember),
    url(r'^updateUserName', views.updateUserName),
    url(r'^searchGroup', views.searchGroup),
    url(r'^viewChoose', views.viewChoose),
    url(r'^checkPush', views.checkPush),
    # url(r'^getOwnGroup', views.getOwnGroup),
    # url(r'^getChoice', views.getChoice),


)
