from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
import os
from surveys.models import SurveyResponse


class Command(BaseCommand):
    help = 'Import survey data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    
    def get_mentor_name(self, mentor_value, mentor_name_text):
        """Get mentor name - handles both string (new format) and integer (old format) values"""
        # If mentor_value is a string (new format), use it directly
        if isinstance(mentor_value, str):
            # If it's "Other", use mentor_name_text if available
            if mentor_value.strip().lower() == 'other':
            return mentor_name_text if mentor_name_text else 'Other'
            return mentor_value
        
        # If mentor_value is an integer (old format), we can't map without the file
        # Use mentor_name_text if available, otherwise return empty
        if mentor_name_text:
            return mentor_name_text
        return ''
    
    def get_topic_name(self, topic_value):
        """Get topic name - handles both string (new format) and integer (old format) values"""
        # If topic_value is a string (new format), use it directly
        if isinstance(topic_value, str):
            return topic_value
        
        # If topic_value is an integer (old format), use hardcoded mapping for backward compatibility
        topic_mapping = {
            1: 'Data Engineering and Visualization',
            2: 'Business Intelligence and Analytics', 
            3: 'Machine Learning and AI',
            4: 'Predictive and Advanced Analytics',
            5: 'Software Development and Web Design'
        }
        return topic_mapping.get(topic_value, '')
    
    def normalize_value(self, value, min_val=1, max_val=5):
        """Normalize value from min_val-max_val range to -1 to 1"""
        if pd.isna(value) or value == '':
            return None
        try:
            val = float(value)
            return 2 * (val - min_val) / (max_val - min_val) - 1
        except (ValueError, TypeError):
            return None
    
    def normalize_rating(self, value, min_val=1, max_val=3):
        """Normalize rating from min_val-max_val range to -1 to 1"""
        if pd.isna(value) or value == '':
            return None
        try:
            val = float(value)
            return 2 * (val - min_val) / (max_val - min_val) - 1
        except (ValueError, TypeError):
            return None

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'File {csv_file} does not exist')
            )
            return

        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Skip the first two rows (headers and descriptions)
            df = df.iloc[2:].reset_index(drop=True)
            
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Skip rows without survey type
                    if pd.isna(row['Q1.1']):
                        continue
                    
                    survey_type = int(row['Q1.1'])
                    
                    # Get mentor and topic mappings - depends on survey type
                    # Handle both string (new format) and integer (old format) values
                    if survey_type == 1:  # Starting survey
                        mentor_raw = row['Q2.3'] if pd.notna(row['Q2.3']) else None
                        mentor_choice = int(mentor_raw) if mentor_raw and str(mentor_raw).isdigit() else mentor_raw
                        mentor_name_text = row['Q2.3.a'] if pd.notna(row['Q2.3.a']) else ''
                    else:  # Ending survey
                        mentor_raw = row['Q3.3'] if pd.notna(row['Q3.3']) else None
                        mentor_choice = int(mentor_raw) if mentor_raw and str(mentor_raw).isdigit() else mentor_raw
                        mentor_name_text = row['Q3.3.a'] if pd.notna(row['Q3.3.a']) else ''
                    
                    project_mentor = self.get_mentor_name(mentor_choice, mentor_name_text)
                    
                    # Get topic based on survey type
                    if survey_type == 1:  # Starting survey
                        topic_raw = row['Q2.6'] if pd.notna(row['Q2.6']) else None
                        topic_value = int(topic_raw) if topic_raw and str(topic_raw).isdigit() else topic_raw
                    else:  # Ending survey
                        topic_raw = row['Q3.8'] if pd.notna(row['Q3.8']) else None
                        topic_value = int(topic_raw) if topic_raw and str(topic_raw).isdigit() else topic_raw
                    topic = self.get_topic_name(topic_value)
                    
                    # Map CSV columns to model fields
                    response_data = {
                        'start_date': pd.to_datetime(row['StartDate']),
                        'end_date': pd.to_datetime(row['EndDate']),
                        'status': int(row['Status']) if pd.notna(row['Status']) else None,
                        'progress': int(row['Progress']) if pd.notna(row['Progress']) else None,
                        'duration_seconds': int(row['Duration (in seconds)']) if pd.notna(row['Duration (in seconds)']) else None,
                        'finished': bool(int(row['Finished'])) if pd.notna(row['Finished']) else False,
                        'recorded_date': pd.to_datetime(row['RecordedDate']),
                        'response_id': row['ResponseId'],
                        'distribution_channel': row['DistributionChannel'],
                        'user_language': row['UserLanguage'],
                        'recaptcha_score': float(row['Q_RecaptchaScore']) if pd.notna(row['Q_RecaptchaScore']) else None,
                        'survey_type': survey_type,
                        # A-number and project title depend on survey type
                        'a_number': row['Q2.1'] if survey_type == 1 and pd.notna(row['Q2.1']) else (row['Q3.1'] if survey_type == 2 and pd.notna(row['Q3.1']) else ''),
                        'project_title': row['Q2.2'] if survey_type == 1 and pd.notna(row['Q2.2']) else (row['Q3.2'] if survey_type == 2 and pd.notna(row['Q3.2']) else ''),
                        'mentor_choice': mentor_choice,
                        'mentor_other_text': row['Q2.3_20_TEXT'] if survey_type == 1 and pd.notna(row['Q2.3_20_TEXT']) else '',
                        'mentor_name': mentor_name_text,
                        'project_mentor': project_mentor,
                        'topic': topic,
                        'is_first_project': bool(int(row['Q2.4'])) if pd.notna(row['Q2.4']) else None,
                        'topics_working_on': int(row['Q2.6']) if pd.notna(row['Q2.6']) else None,
                        'confidence_topics': int(row['Q2.7']) if pd.notna(row['Q2.7']) else None,
                        'enough_resources': int(row['Q2.8']) if pd.notna(row['Q2.8']) else None,
                        'hope_to_gain': row['Q2.9'] if pd.notna(row['Q2.9']) else '',
                        'additional_comments_starting': row['Q2.10'] if pd.notna(row['Q2.10']) else '',
                        # Ending survey fields
                        'gained_learned': row['Q3.5'] if pd.notna(row['Q3.5']) else '',
                        'what_went_well': row['Q3.6'] if pd.notna(row['Q3.6']) else '',
                        'what_could_improve': row['Q3.7'] if pd.notna(row['Q3.7']) else '',
                        'topics_worked_on': int(row['Q3.8']) if pd.notna(row['Q3.8']) else None,
                        'hard_skills_improved': int(row['Q3.9']) if pd.notna(row['Q3.9']) else None,
                        'soft_skills_improved': int(row['Q3.10']) if pd.notna(row['Q3.10']) else None,
                        'confidence_job_placement': int(row['Q3.11']) if pd.notna(row['Q3.11']) else None,
                        # Rating fields
                        'rating_onboarding': int(row['Q3.12_1']) if pd.notna(row['Q3.12_1']) else None,
                        'rating_initiation': int(row['Q3.12_2']) if pd.notna(row['Q3.12_2']) else None,
                        'rating_mentorship': int(row['Q3.12_3']) if pd.notna(row['Q3.12_3']) else None,
                        'rating_team': int(row['Q3.12_4']) if pd.notna(row['Q3.12_4']) else None,
                        'rating_communications': int(row['Q3.12_5']) if pd.notna(row['Q3.12_5']) else None,
                        'rating_expectations': int(row['Q3.12_6']) if pd.notna(row['Q3.12_6']) else None,
                        'rating_sponsor': int(row['Q3.12_7']) if pd.notna(row['Q3.12_7']) else None,
                        'rating_workload': int(row['Q3.12_8']) if pd.notna(row['Q3.12_8']) else None,
                        'recommend_asc': int(row['Q3.13']) if pd.notna(row['Q3.13']) else None,
                        'additional_comments_ending': row['Q3.14'] if pd.notna(row['Q3.14']) else '',
                        # Normalized fields
                        'normalized_hard_skills': self.normalize_value(row['Q3.9']),
                        'normalized_soft_skills': self.normalize_value(row['Q3.10']),
                        'normalized_confidence': self.normalize_value(row['Q3.11']),
                        'normalized_onboarding': self.normalize_rating(row['Q3.12_1']),
                        'normalized_initiation': self.normalize_rating(row['Q3.12_2']),
                        'normalized_mentorship': self.normalize_rating(row['Q3.12_3']),
                        'normalized_team': self.normalize_rating(row['Q3.12_4']),
                        'normalized_communications': self.normalize_rating(row['Q3.12_5']),
                        'normalized_expectations': self.normalize_rating(row['Q3.12_6']),
                        'normalized_sponsor': self.normalize_rating(row['Q3.12_7']),
                        'normalized_workload': self.normalize_rating(row['Q3.12_8']),
                    }
                    
                    # Create or update the response
                    response_obj, created = SurveyResponse.objects.update_or_create(
                        response_id=response_data['response_id'],
                        defaults=response_data
                    )
                    
                    if created:
                        imported_count += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error importing row {index + 3}: {str(e)}')
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {imported_count} survey responses')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to process CSV file: {str(e)}')
            )

