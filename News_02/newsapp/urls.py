from django.urls import path
# Импортируем созданное нами представление
from .views import *
   # PostDetail
from . import views


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='posts'),
   #path('<int:pk>', PostDetail.as_view()),
   path('post/<int:pk>', views.post, name='post'),
   path('search/', PostSearch.as_view(), name='search'),
   path('add/', PostCreate.as_view(), name='add'),
   path('edit/<int:pk>', PostUpdate.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
   path('user/', UserUpdateView.as_view(), name='user_update'),
   path('category/', CategorySubscribeView.as_view()),
   path('category/<int:pk>', subscribe_category, name='subscribe_category'),
]