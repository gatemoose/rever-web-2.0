from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('store/', views.store, name='store'),
    path('download/', views.download, name='download'),
    path('run/', views.run, name='run')
]
