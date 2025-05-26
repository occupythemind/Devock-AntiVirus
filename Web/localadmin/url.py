from django.urls import path
from localadmin import views

app_name="localadmin"
urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', views.auth, name='auth'),
    path('logs/<int:num>/', views.logs, name='logs'),
    path('users/', views.all_users, name='users'),
    path('processes/', views.view_processes, name='processes'),
    path('users/<int:id>/', views.info_user, name='iuser'),
    path('logout/', views.user_logout, name='logout'),
    path('read-the-docs/', views.read_the_docs, name='docs'),
]
