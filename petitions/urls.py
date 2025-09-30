from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='petitions.index'),
    path('create/', views.create_petition, name='petitions.create'),
    path('<int:id>/', views.show, name='petitions.show'),
    path('<int:id>/edit/', views.edit_petition, name='petitions.edit_petition'),
    path('<int:id>/delete/', views.delete_petition, name='petitions.delete_petition'),
    path('<int:id>/upvote/', views.upvote, name='petitions.upvote'),
    path('<int:id>/downvote/', views.downvote, name='petitions.downvote'),
]