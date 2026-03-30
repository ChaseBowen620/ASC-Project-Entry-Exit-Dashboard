from django.urls import path

from . import views

urlpatterns = [
    path('token/', views.DashboardTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/ping/', views.auth_ping, name='auth-ping'),
    path('auth/logout/', views.logout_view, name='auth-logout'),

    # Test endpoint
    path('test/', views.test_api, name='test-api'),
    
    # Survey responses
    path('responses/', views.SurveyResponseListCreateView.as_view(), name='survey-response-list'),
    path('responses/<int:pk>/', views.SurveyResponseDetailView.as_view(), name='survey-response-detail'),
    
    # Survey choices
    path('choices/', views.SurveyChoiceListView.as_view(), name='survey-choice-list'),
    
    # Import functionality
    path('import/', views.import_qualtrics_csv, name='import-qualtrics-csv'),
    
    # Webhook endpoint for Qualtrics
    path('webhook/qualtrics/', views.qualtrics_webhook, name='qualtrics-webhook'),
    
    # Dashboard endpoints
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('dashboard/analytics/', views.survey_analytics, name='survey-analytics'),
    path('available-data/', views.available_data, name='available-data'),
]
