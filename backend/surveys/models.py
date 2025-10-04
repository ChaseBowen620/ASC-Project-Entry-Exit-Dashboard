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
    project_mentor = models.CharField(max_length=200, blank=True, help_text="Mapped mentor name from mentor_choice")
    topic = models.CharField(max_length=200, blank=True, help_text="Mapped topic name from topics_working_on or topics_worked_on")
    
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
    
    # Normalized fields (scaled from -1 to 1)
    normalized_hard_skills = models.FloatField(null=True, blank=True, help_text="Normalized Q3.9 (-1 to 1)")
    normalized_soft_skills = models.FloatField(null=True, blank=True, help_text="Normalized Q3.10 (-1 to 1)")
    normalized_confidence = models.FloatField(null=True, blank=True, help_text="Normalized Q3.11 (-1 to 1)")
    normalized_onboarding = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_1 (-1 to 1)")
    normalized_initiation = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_2 (-1 to 1)")
    normalized_mentorship = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_3 (-1 to 1)")
    normalized_team = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_4 (-1 to 1)")
    normalized_communications = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_5 (-1 to 1)")
    normalized_expectations = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_6 (-1 to 1)")
    normalized_sponsor = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_7 (-1 to 1)")
    normalized_workload = models.FloatField(null=True, blank=True, help_text="Normalized Q3.12_8 (-1 to 1)")
    
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
    
    def get_mentor_name_from_choice(self):
        """Get mentor name from mentor choice"""
        mentor_names = {
            1: 'Andy Brim',
            2: 'Tyler Brough', 
            3: 'Polly Conrad',
            4: 'Chris Corcoran',
            5: 'Doug Derrick',
            6: 'Morgan Diederich',
            7: 'Marc Dotson',
            8: 'Kelly Fadel',
            9: 'Carly Fox',
            10: 'Chelsea Harding',
            11: 'Pedram Jahangiry',
            12: 'Sharad Jones',
            13: 'Toa Pita',
            14: 'Brinley Zabriskie',
            15: 'Other'
        }
        
        if self.mentor_choice == 15:
            return self.mentor_name if self.mentor_name else 'Other'
        elif self.mentor_choice and self.mentor_choice in mentor_names:
            return mentor_names[self.mentor_choice]
        return ''
    
    def get_topic_name_from_value(self):
        """Get topic name from topic value"""
        topic_mapping = {
            1: 'Data Engineering and Visualization',
            2: 'Business Intelligence and Analytics', 
            3: 'Machine Learning and AI',
            4: 'Predictive and Advanced Analytics',
            5: 'Software Development and Web Design'
        }
        
        # Use appropriate topic field based on survey type
        topic_value = self.topics_working_on if self.survey_type == 1 else self.topics_worked_on
        return topic_mapping.get(topic_value, '')
    
    def normalize_value(self, value, min_val=1, max_val=5):
        """Normalize value from min_val-max_val range to -1 to 1"""
        if value is None:
            return None
        return 2 * (value - min_val) / (max_val - min_val) - 1
    
    def normalize_rating(self, value, min_val=1, max_val=3):
        """Normalize rating from min_val-max_val range to -1 to 1"""
        if value is None:
            return None
        return 2 * (value - min_val) / (max_val - min_val) - 1
    
    def save(self, *args, **kwargs):
        # Auto-populate project_mentor and topic fields
        if not self.project_mentor:
            self.project_mentor = self.get_mentor_name_from_choice()
        
        if not self.topic:
            self.topic = self.get_topic_name_from_value()
        
        # Auto-populate normalized fields for ending surveys
        if self.survey_type == 2:
            if self.hard_skills_improved is not None:
                self.normalized_hard_skills = self.normalize_value(self.hard_skills_improved)
            if self.soft_skills_improved is not None:
                self.normalized_soft_skills = self.normalize_value(self.soft_skills_improved)
            if self.confidence_job_placement is not None:
                self.normalized_confidence = self.normalize_value(self.confidence_job_placement)
            
            # Normalize rating fields
            if self.rating_onboarding is not None:
                self.normalized_onboarding = self.normalize_rating(self.rating_onboarding)
            if self.rating_initiation is not None:
                self.normalized_initiation = self.normalize_rating(self.rating_initiation)
            if self.rating_mentorship is not None:
                self.normalized_mentorship = self.normalize_rating(self.rating_mentorship)
            if self.rating_team is not None:
                self.normalized_team = self.normalize_rating(self.rating_team)
            if self.rating_communications is not None:
                self.normalized_communications = self.normalize_rating(self.rating_communications)
            if self.rating_expectations is not None:
                self.normalized_expectations = self.normalize_rating(self.rating_expectations)
            if self.rating_sponsor is not None:
                self.normalized_sponsor = self.normalize_rating(self.rating_sponsor)
            if self.rating_workload is not None:
                self.normalized_workload = self.normalize_rating(self.rating_workload)
        
        super().save(*args, **kwargs)


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

