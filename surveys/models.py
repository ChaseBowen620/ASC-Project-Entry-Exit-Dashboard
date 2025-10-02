from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SurveyResponse(models.Model):
    """Main model for storing ASC survey responses"""
    
    # Qualtrics metadata
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.IntegerField()
    progress = models.IntegerField()
    duration_seconds = models.IntegerField()
    finished = models.BooleanField()
    recorded_date = models.DateTimeField()
    response_id = models.CharField(max_length=100, unique=True)
    distribution_channel = models.CharField(max_length=50)
    user_language = models.CharField(max_length=10)
    recaptcha_score = models.FloatField(null=True, blank=True)
    
    # Survey type (1 = starting project, 2 = ending project)
    survey_type = models.IntegerField(
        choices=[(1, 'Starting Project'), (2, 'Ending Project')],
        help_text="1 = Starting project, 2 = Ending project"
    )
    
    # Common fields for both survey types
    a_number = models.CharField(max_length=20, blank=True)
    project_title = models.TextField(blank=True)
    mentor_choice = models.IntegerField(null=True, blank=True)
    mentor_other_text = models.TextField(blank=True)
    mentor_name = models.CharField(max_length=200, blank=True)
    
    # Starting project specific fields
    is_first_project = models.BooleanField(null=True, blank=True)
    topics_working_on = models.IntegerField(null=True, blank=True)
    confidence_topics = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Scale 1-5"
    )
    enough_resources = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Scale 1-5"
    )
    hope_to_gain = models.TextField(blank=True)
    additional_comments_starting = models.TextField(blank=True)
    
    # Ending project specific fields
    gained_learned = models.TextField(blank=True)
    what_went_well = models.TextField(blank=True)
    what_could_improve = models.TextField(blank=True)
    topics_worked_on = models.IntegerField(null=True, blank=True)
    hard_skills_improved = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Scale 1-5"
    )
    soft_skills_improved = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Scale 1-5"
    )
    confidence_job_placement = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Scale 1-5"
    )
    
    # Rating fields (1-3 scale)
    rating_onboarding = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_initiation = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_mentorship = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_team = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_communications = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_expectations = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_sponsor = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    rating_workload = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="1=Poor, 2=Fair, 3=Excellent"
    )
    
    # Recommendation
    recommend_asc = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Likelihood to recommend ASC (1-5 scale)"
    )
    
    # Additional feedback
    additional_comments_ending = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-recorded_date']
        verbose_name = "Survey Response"
        verbose_name_plural = "Survey Responses"
    
    def __str__(self):
        return f"{self.get_survey_type_display()} - {self.a_number} - {self.response_id}"
    
    @property
    def is_starting_survey(self):
        return self.survey_type == 1
    
    @property
    def is_ending_survey(self):
        return self.survey_type == 2


class SurveyChoice(models.Model):
    """Model to store choice mappings for coded values"""
    
    question_id = models.CharField(max_length=50)
    choice_value = models.IntegerField()
    choice_text = models.CharField(max_length=200)
    question_text = models.TextField()
    
    class Meta:
        unique_together = ['question_id', 'choice_value']
        verbose_name = "Survey Choice"
        verbose_name_plural = "Survey Choices"
    
    def __str__(self):
        return f"{self.question_id}: {self.choice_value} - {self.choice_text}"

