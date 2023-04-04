from django.urls import path
from . import views

urlpatterns = [
	# path('', views.redirect_to_device, name='dashboard'),
	path('', views.DashboardView.as_view(), name='dashboard'),
	path('comming-soon/', views.ComingSoonView.as_view(), name='coming_soon'),
	path('log-chart-data/<int:user_id>', views.LogChartDataAPI.as_view(), name='event_log_chart'),
]
