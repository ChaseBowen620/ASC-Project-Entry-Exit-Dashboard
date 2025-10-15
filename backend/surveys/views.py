import pandas as pd
import os
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SurveyResponse, SurveyChoice
from .serializers import (
    SurveyResponseSerializer, 
    SurveyResponseListSerializer, 
    SurveyChoiceSerializer,
    QualtricsImportSerializer
)
from datetime import datetime


def apply_filters(queryset, filters):
    """Apply filters to the queryset based on request parameters"""
    if filters.get('mentor'):
        # Filter by mentor using project_mentor field
        queryset = queryset.filter(project_mentor__icontains=filters['mentor'])
    
    if filters.get('topic'):
        # Filter by topic using topic field
        queryset = queryset.filter(topic__icontains=filters['topic'])
    
    if filters.get('projectName'):
        queryset = queryset.filter(project_title__icontains=filters['projectName'])
    
    if filters.get('startDate'):
        try:
            start_date = datetime.strptime(filters['startDate'], '%Y-%m-%d').date()
            queryset = queryset.filter(end_date__date__gte=start_date)
        except ValueError:
            pass
    
    if filters.get('endDate'):
        try:
            end_date = datetime.strptime(filters['endDate'], '%Y-%m-%d').date()
            queryset = queryset.filter(end_date__date__lte=end_date)
        except ValueError:
            pass
    
    return queryset


class SurveyResponseListCreateView(generics.ListCreateAPIView):
    """List all survey responses or create a new one"""
    queryset = SurveyResponse.objects.all()  # Both starting and ending surveys
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SurveyResponseListSerializer
        return SurveyResponseSerializer


class SurveyResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a survey response"""
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer


class SurveyChoiceListView(generics.ListAPIView):
    """List all survey choices for reference"""
    queryset = SurveyChoice.objects.all()
    serializer_class = SurveyChoiceSerializer


@api_view(['POST'])
def import_qualtrics_csv(request):
    """Import Qualtrics CSV data"""
    if request.method == 'POST':
        serializer = QualtricsImportSerializer(data=request.data)
        
        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']
            
            try:
                # Read CSV file
                df = pd.read_csv(csv_file)
                
                # Skip the first two rows (headers and descriptions)
                df = df.iloc[2:].reset_index(drop=True)
                
                imported_count = 0
                errors = []
                
                with transaction.atomic():
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
                            errors.append(f"Row {index + 3}: {str(e)}")
                            continue
                
                return Response({
                    'message': f'Successfully imported {imported_count} survey responses',
                    'imported_count': imported_count,
                    'errors': errors[:10] if errors else [],  # Limit errors shown
                    'total_errors': len(errors)
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    'error': f'Failed to process CSV file: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def dashboard_stats(request):
    """Get dashboard statistics"""
    try:
        # Apply filters - only ending surveys
        queryset = apply_filters(SurveyResponse.objects.filter(survey_type=2), request.GET)
        
        total_responses = queryset.count()
        starting_responses = 0  # We're only showing ending surveys
        ending_responses = queryset.count()
        
        # Average ratings for ending surveys
        ending_surveys = queryset  # Already filtered to ending surveys
        
        avg_ratings = {}
        rating_fields = [
            'rating_onboarding', 'rating_initiation', 'rating_mentorship',
            'rating_team', 'rating_communications', 'rating_expectations',
            'rating_sponsor', 'rating_workload'
        ]
        
        for field in rating_fields:
            try:
                values = list(ending_surveys.exclude(**{field: None}).values_list(field, flat=True))
                if values:
                    avg_ratings[field] = round(sum(values) / len(values), 2)
            except Exception as e:
                avg_ratings[field] = None
        
        # Average recommendation score
        try:
            recommend_scores = list(ending_surveys.exclude(recommend_asc=None).values_list('recommend_asc', flat=True))
            avg_recommendation = round(sum(recommend_scores) / len(recommend_scores), 2) if recommend_scores else None
        except Exception as e:
            avg_recommendation = None
        
        completion_rate = 100  # Since we're only showing ending surveys, completion rate is 100%
        
        return Response({
            'total_responses': total_responses,
            'starting_responses': starting_responses,
            'ending_responses': ending_responses,
            'average_ratings': avg_ratings,
            'average_recommendation': avg_recommendation,
            'completion_rate': completion_rate
        })
    except Exception as e:
        return Response({
            'error': f'Error calculating dashboard stats: {str(e)}',
            'total_responses': 0,
            'starting_responses': 0,
            'ending_responses': 0,
            'average_ratings': {},
            'average_recommendation': None,
            'completion_rate': 0
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def test_api(request):
    """Test endpoint to verify API is working"""
    return Response({
        'message': 'API is working!',
        'timestamp': pd.Timestamp.now().isoformat(),
        'total_responses': SurveyResponse.objects.count()
    })


@api_view(['GET'])
def survey_analytics(request):
    """Get detailed analytics for the dashboard"""
    try:
        # Apply filters - only ending surveys
        queryset = apply_filters(SurveyResponse.objects.filter(survey_type=2), request.GET)
        
        # Topic analysis - only ending surveys
        topics_ending = list(queryset.filter(
            topics_worked_on__isnull=False
        ).values_list('topics_worked_on', flat=True))
        
        # Confidence analysis (from ending surveys - Q3.11)
        confidence_data = list(queryset.filter(
            confidence_job_placement__isnull=False
        ).values_list('confidence_job_placement', flat=True))
        
        # Skills improvement analysis
        hard_skills_data = list(queryset.filter(
            hard_skills_improved__isnull=False
        ).values_list('hard_skills_improved', flat=True))
        
        soft_skills_data = list(queryset.filter(
            soft_skills_improved__isnull=False
        ).values_list('soft_skills_improved', flat=True))
        
        return Response({
            'topics_ending': topics_ending,
            'confidence_levels': confidence_data,
            'hard_skills_improvement': hard_skills_data,
            'soft_skills_improvement': soft_skills_data,
        })
    except Exception as e:
        return Response({
            'error': f'Error calculating analytics: {str(e)}',
            'topics_ending': [],
            'confidence_levels': [],
            'hard_skills_improvement': [],
            'soft_skills_improvement': [],
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def available_data(request):
    """Get available data for filter dropdowns"""
    try:
        # Get all survey responses (both starting and ending)
        queryset = SurveyResponse.objects.all()
        
        # Get unique mentors from project_mentor field
        mentors = list(queryset.exclude(
            Q(project_mentor='') | Q(project_mentor__isnull=True)
        ).values_list('project_mentor', flat=True).distinct())
        
        # Get unique project titles
        projects = list(queryset.exclude(
            Q(project_title='') | Q(project_title__isnull=True)
        ).values_list('project_title', flat=True).distinct())
        
        # Get unique topics from topic field
        topics = list(queryset.exclude(
            Q(topic='') | Q(topic__isnull=True)
        ).values_list('topic', flat=True).distinct())
        
        return Response({
            'mentors': sorted(mentors),
            'projects': sorted(projects),
            'topics': sorted(topics)
        })
    except Exception as e:
        return Response({
            'error': f'Error getting available data: {str(e)}',
            'mentors': [],
            'projects': [],
            'topics': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def qualtrics_webhook(request):
    """Webhook endpoint to receive new survey responses from Qualtrics"""
    try:
        # Get the raw data from the request
        data = request.data
        
        # Log the incoming webhook for debugging
        print(f"=== WEBHOOK DEBUG ===")
        print(f"Received webhook data: {data}")
        print(f"Data type: {type(data)}")
        print(f"Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        print(f"Request content type: {request.content_type}")
        print(f"Request method: {request.method}")
        
        # Handle different data formats that Qualtrics might send
        if not isinstance(data, dict):
            print(f"Data is not a dict, converting...")
            data = dict(data) if hasattr(data, 'items') else {}
        
        # If data is empty, try to get it from request.POST (form data)
        if not data and request.POST:
            print(f"Using request.POST data: {dict(request.POST)}")
            data = dict(request.POST)
            # Convert single-item lists to strings (Django form behavior)
            for key, value in data.items():
                if isinstance(value, list) and len(value) == 1:
                    data[key] = value[0]
        
        print(f"Final processed data: {data}")
        print(f"=== END WEBHOOK DEBUG ===")
        
        # Helper function to safely parse datetime
        def safe_datetime(value):
            if not value or value == '':
                return None
            try:
                return pd.to_datetime(value)
            except:
                return None
        
        # Helper function to safely parse integer
        def safe_int(value):
            if not value or value == '' or value == '0':
                return None
            try:
                return int(value)
            except:
                return None
        
        # Helper function to safely parse float
        def safe_float(value):
            if not value or value == '' or value == '0':
                return None
            try:
                return float(value)
            except:
                return None
        
        # Helper function to safely parse boolean
        def safe_bool(value):
            if not value or value == '':
                return None
            try:
                return bool(int(value))
            except:
                return None
        
        # Helper function to map Q1.1 survey type
        def map_survey_type(value):
            if not value:
                return None
            value_lower = str(value).lower().strip()
            if 'starting' in value_lower:
                return 1  # Starting survey
            elif 'ending' in value_lower:
                return 2  # Ending survey
            else:
                return None
        
        # Helper function to map Q3.9-Q3.11 agreement scale
        def map_agreement_scale(value):
            if not value:
                return None
            value_lower = str(value).lower().strip()
            if 'strongly disagree' in value_lower:
                return 1  # Will be normalized to -1
            elif 'somewhat disagree' in value_lower:
                return 2  # Will be normalized to -0.5
            elif 'neither agree nor disagree' in value_lower or 'neither' in value_lower:
                return 3  # Will be normalized to 0
            elif 'somewhat agree' in value_lower:
                return 4  # Will be normalized to 0.5
            elif 'strongly agree' in value_lower:
                return 5  # Will be normalized to 1
            else:
                return None
        
        # Helper function to map Q3.12 rating scale (1-3)
        def map_rating_scale(value):
            if value is None or value == '':
                return None
            value_str = str(value).strip()
            # Handle formats like "1 (Poor)", "2 (Neutral)", "2 (Fair)" or just "1" or "0"
            if '(' in value_str:
                # Extract number from "1 (Poor)" or "2 (Neutral)" format
                number_part = value_str.split('(')[0].strip()
                try:
                    return int(number_part)
                except:
                    return None
            else:
                try:
                    return int(value_str)
                except:
                    return None
        
        # Helper function to map mentor names to integers
        def map_mentor_to_int(mentor_name):
            if not mentor_name:
                return None
            try:
                # Read mentor values from file
                mentor_file_path = os.path.join(os.path.dirname(__file__), '..', 'Mentor Values.txt')
                with open(mentor_file_path, 'r') as f:
                    mentors = [line.strip() for line in f.readlines() if line.strip()]
                
                # Create mapping (1-indexed)
                mentor_mapping = {mentor: idx + 1 for idx, mentor in enumerate(mentors)}
                return mentor_mapping.get(mentor_name, len(mentors))  # Default to last (Other) if not found
            except Exception as e:
                print(f"Error reading mentor values: {e}")
                return None
        
        # Helper function to map topic names to integers
        def map_topic_to_int(topic_name):
            if not topic_name:
                return None
            try:
                # Read topic values from file
                topic_file_path = os.path.join(os.path.dirname(__file__), '..', 'Topic Values.txt')
                with open(topic_file_path, 'r') as f:
                    topics = [line.strip() for line in f.readlines() if line.strip()]
                
                # Create mapping (1-indexed)
                topic_mapping = {topic: idx + 1 for idx, topic in enumerate(topics)}
                return topic_mapping.get(topic_name, 1)  # Default to first topic if not found
            except Exception as e:
                print(f"Error reading topic values: {e}")
                return None
        
        # Get current timestamp for required datetime fields
        from django.utils import timezone
        current_time = timezone.now()
        
        # Check if this is an ending survey - only process ending surveys
        survey_type = map_survey_type(data.get('Q1.1'))
        if survey_type != 2:  # Not an ending survey
            return Response({
                'success': True,
                'message': f'Survey type {survey_type} ({"Starting" if survey_type == 1 else "Unknown"}) - not processing. Only ending surveys are stored.',
                'survey_type': survey_type,
                'skipped': True
            }, status=status.HTTP_200_OK)
        
        # Extract survey response data from Qualtrics webhook format
        # Qualtrics typically sends data in this format
        response_data = {
            # Required fields with auto-populated defaults
            'start_date': safe_datetime(data.get('StartDate')) or current_time,
            'end_date': safe_datetime(data.get('EndDate')) or current_time,
            'status': safe_int(data.get('Status')) or 1,
            'progress': safe_int(data.get('Progress')) or 100,
            'duration_seconds': safe_int(data.get('Duration (in seconds)')) or 0,
            'finished': safe_bool(data.get('Finished')) if data.get('Finished') is not None else True,
            'recorded_date': safe_datetime(data.get('RecordedDate')) or current_time,
            # Handle both ResponseId and ResponseID field names
            'response_id': data.get('ResponseId') or data.get('ResponseID', ''),
            'distribution_channel': data.get('DistributionChannel', 'qualtrics'),
            'user_language': data.get('UserLanguage', 'EN'),
            'recaptcha_score': safe_float(data.get('Q_RecaptchaScore')),
            'survey_type': survey_type,  # Already validated as 2 (ending survey)
            'a_number': data.get('Q3.1', ''),  # A Number (may be empty in some formats)
            'project_title': data.get('Q3.2', ''),  # Project title not available in ending surveys
            'mentor_choice': map_mentor_to_int(data.get('Q3.3', '')),
            'mentor_other_text': data.get('Q3.3_20_TEXT', ''),
            'mentor_name': data.get('Q3.3.a', ''),  # Mentor name from ending survey
            'project_mentor': data.get('Q3.3', ''),  # Keep string for display
            'is_first_project': None,  # Not used for ending surveys
            'topics_working_on': None,  # Not used for ending surveys
            'topics_worked_on': map_topic_to_int(data.get('Q3.8', '')),  # Map topic to integer
            'topic': data.get('Q3.8', ''),  # Keep string for display
            'confidence_topics': None,  # Not used for ending surveys
            'enough_resources': None,  # Not used for ending surveys
            'hope_to_gain': '',  # Not used for ending surveys
            'additional_comments_starting': '',  # Not used for ending surveys
            # Ending survey fields - using string values directly
            'gained_learned': data.get('Q3.5', ''),  # Q3.5 or Q3.2 for gained/learned
            'what_went_well': data.get('Q3.6', ''),
            'what_could_improve': data.get('Q3.7', ''),
            'hard_skills_improved': map_agreement_scale(data.get('Q3.9')),
            'soft_skills_improved': map_agreement_scale(data.get('Q3.10')),
            'confidence_job_placement': map_agreement_scale(data.get('Q3.11')),
            # Rating fields - using the new mapping function
            'rating_onboarding': map_rating_scale(data.get('Q3.12.a')),
            'rating_initiation': map_rating_scale(data.get('Q3.12.b')),
            'rating_mentorship': map_rating_scale(data.get('Q3.12.c')),
            'rating_team': map_rating_scale(data.get('Q3.12.d')),
            'rating_communications': map_rating_scale(data.get('Q3.12.e')),
            'rating_expectations': map_rating_scale(data.get('Q3.12.f')),
            'rating_sponsor': map_rating_scale(data.get('Q3.12.g')),
            'rating_workload': map_rating_scale(data.get('Q3.12.h')),
            'recommend_asc': safe_int(data.get('Q3.13')),
            'additional_comments_ending': data.get('Q3.14', ''),
        }
        
        # Create or update the response
        response_obj, created = SurveyResponse.objects.update_or_create(
            response_id=response_data['response_id'],
            defaults=response_data
        )
        
        if created:
            message = f"New survey response created with ID: {response_obj.id}"
        else:
            message = f"Survey response updated with ID: {response_obj.id}"
        
        return Response({
            'success': True,
            'message': message,
            'response_id': response_obj.response_id,
            'survey_type': response_obj.survey_type,
            'created': created
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return Response({
            'success': False,
            'error': f'Failed to process webhook data: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
