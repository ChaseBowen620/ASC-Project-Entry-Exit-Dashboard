from django.contrib import admin
from .models import SurveyResponse, SurveyChoice


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = [
        'response_id', 'survey_type', 'a_number', 'project_title', 
        'recorded_date', 'finished'
    ]
    list_filter = ['survey_type', 'finished', 'recorded_date', 'distribution_channel']
    search_fields = ['response_id', 'a_number', 'project_title', 'mentor_name']
    readonly_fields = ['response_id', 'created_at', 'updated_at']
    date_hierarchy = 'recorded_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('response_id', 'survey_type', 'a_number', 'project_title')
        }),
        ('Mentor Information', {
            'fields': ('mentor_choice', 'mentor_other_text', 'mentor_name')
        }),
        ('Starting Project Fields', {
            'fields': ('is_first_project', 'topics_working_on', 'confidence_topics', 
                      'enough_resources', 'hope_to_gain', 'additional_comments_starting'),
            'classes': ('collapse',)
        }),
        ('Ending Project Fields', {
            'fields': ('gained_learned', 'what_went_well', 'what_could_improve', 
                      'topics_worked_on', 'hard_skills_improved', 'soft_skills_improved', 
                      'confidence_job_placement', 'additional_comments_ending'),
            'classes': ('collapse',)
        }),
        ('Ratings', {
            'fields': ('rating_onboarding', 'rating_initiation', 'rating_mentorship', 
                      'rating_team', 'rating_communications', 'rating_expectations', 
                      'rating_sponsor', 'rating_workload', 'recommend_asc'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('start_date', 'end_date', 'status', 'progress', 'duration_seconds', 
                      'finished', 'recorded_date', 'distribution_channel', 'user_language', 
                      'recaptcha_score', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SurveyChoice)
class SurveyChoiceAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'choice_value', 'choice_text']
    list_filter = ['question_id']
    search_fields = ['question_id', 'choice_text']

