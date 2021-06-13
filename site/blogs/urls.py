from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.create, name='create'),
    path('success_saved', views.success_saved, name='success_saved'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/blog_delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('<int:pk>/blog_update/', views.BlogUpdateView.as_view(), name='blog_update')
]
