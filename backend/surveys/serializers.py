from django.contrib.auth import get_user_model
from decouple import config
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import SurveyResponse, SurveyChoice


class SurveyChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyChoice
        fields = '__all__'


class SurveyResponseSerializer(serializers.ModelSerializer):
    survey_type_display = serializers.CharField(source='get_survey_type_display', read_only=True)
    
    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SurveyResponseListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    survey_type_display = serializers.CharField(source='get_survey_type_display', read_only=True)
    
    class Meta:
        model = SurveyResponse
        fields = [
            'id', 'response_id', 'survey_type', 'survey_type_display', 
            'a_number', 'project_title', 'project_mentor', 'topic', 'recorded_date', 'finished',
            'confidence_topics', 'enough_resources', 'hard_skills_improved',
            'soft_skills_improved', 'confidence_job_placement', 'recommend_asc',
            'rating_onboarding', 'rating_initiation', 'rating_mentorship', 'rating_team',
            'rating_communications', 'rating_expectations', 'rating_sponsor', 'rating_workload'
        ]


class QualtricsImportSerializer(serializers.Serializer):
    """Serializer for handling Qualtrics CSV imports"""
    csv_file = serializers.FileField()
    
    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        return value


class DashboardTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Issue JWTs when username/password match server-side dashboard credentials."""

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        expected_user = config('DASHBOARD_USERNAME', default='')
        expected_pass = config('DASHBOARD_PASSWORD', default='')
        if not expected_user or not expected_pass:
            raise serializers.ValidationError(
                {'detail': 'Dashboard login is not configured on the server.'}
            )
        if username != expected_user or password != expected_pass:
            raise serializers.ValidationError(
                {'detail': 'No active account found with the given credentials.'}
            )
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username='asc_dashboard_service',
            defaults={'is_active': True, 'is_staff': False, 'is_superuser': False},
        )
        user.set_unusable_password()
        user.save()
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
