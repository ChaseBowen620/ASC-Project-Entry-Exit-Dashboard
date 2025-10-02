import pandas as pd
import io
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import SurveyResponse, SurveyChoice
from .serializers import (
    SurveyResponseSerializer, 
    SurveyResponseListSerializer, 
    SurveyChoiceSerializer,
    QualtricsImportSerializer
)
from django.db.models import Q
from datetime import datetime


def apply_filters(queryset, filters):
    """Apply filters to the queryset based on request parameters"""
    if filters.get('mentor'):
        queryset = queryset.filter(
            Q(mentor_name__icontains=filters['mentor']) |
            Q(mentor_other_text__icontains=filters['mentor'])
        )
    
    if filters.get('topic'):
        # For topic filtering, we need to map topic names to numbers
        # This is a simplified mapping - you might want to create a proper mapping
        topic_mapping = {
            'data_science': 1,
            'web_development': 2,
            'mobile_development': 3,
            'ai_ml': 4,
            'cybersecurity': 5,
            'cloud_computing': 6,
            'other': 7
        }
        topic_value = topic_mapping.get(filters['topic'].lower())
        if topic_value:
            queryset = queryset.filter(
                Q(topics_working_on=topic_value) |
                Q(topics_worked_on=topic_value)
            )
    
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
    queryset = SurveyResponse.objects.all()
    
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
        # Apply filters
        queryset = apply_filters(SurveyResponse.objects.all(), request.GET)
        
        total_responses = queryset.count()
        starting_responses = queryset.filter(survey_type=1).count()
        ending_responses = queryset.filter(survey_type=2).count()
        
        # Average ratings for ending surveys
        ending_surveys = queryset.filter(survey_type=2)
        
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
                print(f"Error calculating {field}: {e}")
                avg_ratings[field] = None
        
        # Average recommendation score
        try:
            recommend_scores = list(ending_surveys.exclude(recommend_asc=None).values_list('recommend_asc', flat=True))
            avg_recommendation = round(sum(recommend_scores) / len(recommend_scores), 2) if recommend_scores else None
        except Exception as e:
            print(f"Error calculating recommendation: {e}")
            avg_recommendation = None
        
        completion_rate = 0
        if starting_responses > 0:
            completion_rate = round((ending_responses / starting_responses * 100), 2)
        
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
        # Apply filters
        queryset = apply_filters(SurveyResponse.objects.all(), request.GET)
        
        # Topic analysis
        topics_starting = list(queryset.filter(
            survey_type=1, topics_working_on__isnull=False
        ).values_list('topics_working_on', flat=True))
        
        topics_ending = list(queryset.filter(
            survey_type=2, topics_worked_on__isnull=False
        ).values_list('topics_worked_on', flat=True))
        
        # Confidence analysis (from ending surveys - Q3.11)
        confidence_data = list(queryset.filter(
            survey_type=2, confidence_job_placement__isnull=False
        ).values_list('confidence_job_placement', flat=True))
        
        # Skills improvement analysis
        hard_skills_data = list(queryset.filter(
            survey_type=2, hard_skills_improved__isnull=False
        ).values_list('hard_skills_improved', flat=True))
        
        soft_skills_data = list(queryset.filter(
            survey_type=2, soft_skills_improved__isnull=False
        ).values_list('soft_skills_improved', flat=True))
        
        return Response({
            'topics_starting': topics_starting,
            'topics_ending': topics_ending,
            'confidence_levels': confidence_data,
            'hard_skills_improvement': hard_skills_data,
            'soft_skills_improvement': soft_skills_data,
        })
    except Exception as e:
        return Response({
            'error': f'Error calculating analytics: {str(e)}',
            'topics_starting': [],
            'topics_ending': [],
            'confidence_levels': [],
            'hard_skills_improvement': [],
            'soft_skills_improvement': [],
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def available_data(request):
    """Get available data for filter dropdowns"""
    try:
        # Get unique mentors
        mentors = list(SurveyResponse.objects.exclude(
            Q(mentor_name='') | Q(mentor_name__isnull=True)
        ).values_list('mentor_name', flat=True).distinct())
        
        # Get unique project titles
        projects = list(SurveyResponse.objects.exclude(
            Q(project_title='') | Q(project_title__isnull=True)
        ).values_list('project_title', flat=True).distinct())
        
        # Get unique topics (we'll need to map the numeric values to names)
        topic_mapping = {
            1: 'Data Science',
            2: 'Web Development', 
            3: 'Mobile Development',
            4: 'AI/ML',
            5: 'Cybersecurity',
            6: 'Cloud Computing',
            7: 'Other'
        }
        
        # Get unique topic values
        topics_starting = list(SurveyResponse.objects.filter(
            topics_working_on__isnull=False
        ).values_list('topics_working_on', flat=True).distinct())
        
        topics_ending = list(SurveyResponse.objects.filter(
            topics_worked_on__isnull=False
        ).values_list('topics_worked_on', flat=True).distinct())
        
        all_topics = set(topics_starting + topics_ending)
        topics = [topic_mapping.get(topic, f'Topic {topic}') for topic in all_topics]
        
        return Response({
            'mentors': mentors,
            'projects': projects,
            'topics': sorted(topics)
        })
    except Exception as e:
        return Response({
            'error': f'Error getting available data: {str(e)}',
            'mentors': [],
            'projects': [],
            'topics': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
