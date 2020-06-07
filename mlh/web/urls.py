from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.login_view, name='signin'),
    path('signout/', views.logout_view, name='signout'),
    path('signup/', views.add_user, name='signup'),
    path('profile/new_pass', views.change_password, name='change_password'),
    path('profile/', views.user_profile, name='user_profile'),
    path('signin/res_pass/', views.reset_password, name='reset_password'),
    path('addgoals/', views.adding_goal, name='add_goal'),
    path('search/', views.search_sport, name='search_sport'),
    path('profile/<int:id>', views.show_profile, name='show_profile'),
    path('profile/<int:id>/add', views.make_friend_request, name='make_friend_request'),
    path('deletegoals/', views.delete_goal, name='delete_goal'),
    path('profile/requests', views.show_friend_request, name='show_requests'),
    path('profile/requests/<int:request_id>/allow', views.allow_friend_request, name='allow_request'),
    path('profile/requests/<int:request_id>/decline', views.decline_friend_request, name='decline_request'),
    path('posts/', views.show_all_posts, name='show_all_posts'),
    path('add_post/', views.add_post, name='add_post'),
    path('post/<int:post_id>', views.show_post, name='show_post')
]
