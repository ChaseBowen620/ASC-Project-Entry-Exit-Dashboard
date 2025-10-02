from django.core.management.base import BaseCommand
import pandas as pd
import os
from surveys.models import SurveyResponse


class Command(BaseCommand):
    help = 'Import survey data from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

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
                        'survey_type': int(row['Q1.1']) if pd.notna(row['Q1.1']) else None,
                        'a_number': row['Q2.1'] if pd.notna(row['Q2.1']) else '',
                        'project_title': row['Q2.2'] if pd.notna(row['Q2.2']) else '',
                        'mentor_choice': int(row['Q2.3']) if pd.notna(row['Q2.3']) else None,
                        'mentor_other_text': row['Q2.3_20_TEXT'] if pd.notna(row['Q2.3_20_TEXT']) else '',
                        'mentor_name': row['Q2.3.a'] if pd.notna(row['Q2.3.a']) else '',
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

