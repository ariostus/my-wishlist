from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<username>/list<int:title>/', views.wishListView, name='wish-list'),
    path('<username>/list<int:title>/wish<int:pk>', views.wishUpdateView, name='wish-detail'),
    path('<username>/list<int:title>/add', views.wishAddView, name='add-wish'),
    path('<username>/', views.userLists, name='user-lists'),
    path('<username>/list<int:title>/delete', views.listDelete, name='list-delete'),
    path('<username>/list<int:title>/edit', views.listEdit, name='list-edit'),
    path('<username>/add', views.listCreate, name='list-add'),
    path('<username>/list<int:title>/wish<int:pk>/delete', views.wishDeleteView, name='wish-delete'),
]