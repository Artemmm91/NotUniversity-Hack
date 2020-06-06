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
    path('profile/<int:id>/add', views.add_friend, name='add_friend'),
]
