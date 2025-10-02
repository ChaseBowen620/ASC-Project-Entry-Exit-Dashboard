from rest_framework import serializers
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
            'a_number', 'project_title', 'recorded_date', 'finished',
            'confidence_topics', 'enough_resources', 'hard_skills_improved',
            'soft_skills_improved', 'confidence_job_placement', 'recommend_asc'
        ]


class QualtricsImportSerializer(serializers.Serializer):
    """Serializer for handling Qualtrics CSV imports"""
    csv_file = serializers.FileField()
    
    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must be a CSV file.")
        return value

