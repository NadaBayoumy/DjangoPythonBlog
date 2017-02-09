"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url
from django.contrib import admin
from . import views

#hossam
from django.contrib.auth import views as auth_views
#end hossam




urlpatterns = [
    #nada
    url(r'^category/$', views.all_category),
    url(r'^new/$', views.new_category),
    url(r'^(?P<c_id>[0-9]+)/edit$', views.edit_category),
    url(r'^(?P<c_id>[0-9]+)/delete/$', views.delete_category),
    url(r'^forbidden_words/$', views.all_forbidden_words),
    url(r'^new_forbidden_word/$', views.new_forbidden_word),
    url(r'^(?P<w_id>[0-9]+)/delete_forbidden_word/$', views.delete_forbidden_word),
    url(r'^(?P<comment_txt>[0-9a-zA-Z ]+)/check_comment/$', views.check_forbidden_words_in_comment),
    
    url(r'^post/$', views.all_post),
    url(r'^new_post/$', views.new_post),
    url(r'^(?P<p_id>[0-9]+)/edit_post$', views.edit_post),
    url(r'^(?P<p_id>[0-9]+)/delete_post/$', views.delete_post),
    #nada
    
    #alalem
    url(r'^$', views.show_categories),       # redirection to specific user home page
    url(r'^(?P<c_id>[0-9]+)/$', views.show_posts), # redirection to posts related to this category
    url(r'^(?P<c_id>[0-9]+)/(?P<p_id>[0-9]+)/$', views.post_display), # redirection to post contents
    url(r'^(?P<c_id>[0-9]+)/subscribe', views.subscribe_category), # redirection to subscribe category
    url(r'^(?P<c_id>[0-9]+)/unsubscribe', views.unsubscribe_category), # redirection to unsubscribe category
    url(r'^(?P<c_id>[0-9]+)/new_post', views.add_new_post),
    url(r'^(?P<c_id>[0-9]+)/(?P<p_id>[0-9]+)/modify_post', views.modify_post),
    url(r'^(?P<c_id>[0-9]+)/(?P<p_id>[0-9]+)/delete_post', views.delete_post),
    url(r'^(?P<c_id>[0-9]+)/(?P<p_id>[0-9]+)/comment$', views.add_comment),
    url(r'^(?P<ca_id>[0-9]+)/(?P<p_id>[0-9]+)/(?P<co_id>[0-9]+)/reply$', views.add_reply),
    #alalem
    
    
    
    #hossam
    url(r'^login/$', views.login_user),
    url(r'^admins/$', views.login_admin),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}),
    url(r'^users/$', views.users_list),
    url(r'^users/edit/(?P<user_id>[0-9]+)$', views.edit_user),
    url(r'^users/edit/ch_pw/(?P<user_id>[0-9]+)$', views.change_pw),
    url(r'^users/new/$', views.create_user),
    url(r'^users/edit/del/(?P<user_id>[0-9]+)$', views.delete_user),
    url(r'^block/(?P<user_id>[0-9]+)$', views.block_user),
    url(r'^promote/(?P<user_id>[0-9]+)$', views.promote_user),
    #end hossam
    
    
    
    
    #simona
     #urls of crud operations on categories
    #urls of register
    url(r'^HomePage/$', views.Home_options ),
    url(r'^registration$',views.registration),
    url(r'^manage$', views.manage),
    #   url(r'^BlogApp/registrationAdmin$', views.registration_admin),
    
    #end simona
    
]
