from django.urls import path
from . import views

urlpatterns = [
	path('', views.DashboardView.as_view(), name='dashboard'),
	path('log-chart-data/<int:user_id>', views.LogChartDataAPI.as_view(), name='event_log_chart'),
]
