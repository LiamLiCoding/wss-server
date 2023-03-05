from django.urls import path
from . import views

urlpatterns = [
    path('websocket/', views.DocWsDataCommunicationView.as_view(), name='doc_websocket_data_com'),
]
