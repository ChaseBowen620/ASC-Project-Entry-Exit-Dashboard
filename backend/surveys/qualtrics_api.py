"""
Qualtrics API integration utilities
"""
import requests
from django.conf import settings
import json


def get_qualtrics_headers():
    """Get headers for Qualtrics API requests"""
    return {
        'X-API-TOKEN': settings.QUALTRICS_API_TOKEN,
        'Content-Type': 'application/json'
    }


def get_qualtrics_responses(survey_id=None, start_date=None, end_date=None):
    """
    Fetch responses from Qualtrics API
    
    Args:
        survey_id: Qualtrics survey ID (defaults to settings.QUALTRICS_SURVEY_ID)
        start_date: Start date filter (ISO format)
        end_date: End date filter (ISO format)
    
    Returns:
        dict: API response with responses data
    """
    if not settings.QUALTRICS_API_TOKEN:
        return {'error': 'Qualtrics API token not configured'}
    
    if not settings.QUALTRICS_DATA_CENTER:
        return {'error': 'Qualtrics data center not configured'}
    
    survey_id = survey_id or settings.QUALTRICS_SURVEY_ID
    if not survey_id:
        return {'error': 'Survey ID not provided'}
    
    base_url = settings.QUALTRICS_API_URL
    endpoint = f"{base_url}/surveys/{survey_id}/export-responses"
    
    # Create export request
    export_data = {
        'format': 'json',
        'useLabels': True
    }
    
    if start_date:
        export_data['startDate'] = start_date
    if end_date:
        export_data['endDate'] = end_date
    
    try:
        # Step 1: Create export
        response = requests.post(
            endpoint,
            headers=get_qualtrics_headers(),
            json=export_data
        )
        
        if response.status_code != 200:
            return {
                'error': f'Failed to create export: {response.status_code}',
                'details': response.text
            }
        
        export_progress_id = response.json().get('result', {}).get('progressId')
        if not export_progress_id:
            return {'error': 'No progress ID returned from export request'}
        
        # Step 2: Check export progress
        progress_endpoint = f"{base_url}/surveys/{survey_id}/export-responses/{export_progress_id}"
        import time
        
        while True:
            progress_response = requests.get(
                progress_endpoint,
                headers=get_qualtrics_headers()
            )
            
            if progress_response.status_code != 200:
                return {
                    'error': f'Failed to check progress: {progress_response.status_code}',
                    'details': progress_response.text
                }
            
            progress_data = progress_response.json()
            status = progress_data.get('result', {}).get('status')
            
            if status == 'complete':
                file_id = progress_data.get('result', {}).get('fileId')
                break
            elif status == 'failed':
                return {'error': 'Export failed'}
            else:
                time.sleep(2)  # Wait 2 seconds before checking again
        
        # Step 3: Download the file
        download_endpoint = f"{base_url}/surveys/{survey_id}/export-responses/{export_progress_id}/file"
        download_response = requests.get(
            download_endpoint,
            headers=get_qualtrics_headers()
        )
        
        if download_response.status_code != 200:
            return {
                'error': f'Failed to download export: {download_response.status_code}',
                'details': download_response.text
            }
        
        # Parse the JSON response
        try:
            responses_data = download_response.json()
            return {
                'success': True,
                'data': responses_data
            }
        except json.JSONDecodeError:
            return {
                'error': 'Failed to parse response data',
                'raw': download_response.text[:500]  # First 500 chars for debugging
            }
    
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}'
        }


def get_qualtrics_response_by_id(survey_id, response_id):
    """
    Get a specific response from Qualtrics by response ID
    
    Args:
        survey_id: Qualtrics survey ID
        response_id: Qualtrics response ID
    
    Returns:
        dict: Response data
    """
    if not settings.QUALTRICS_API_TOKEN:
        return {'error': 'Qualtrics API token not configured'}
    
    if not settings.QUALTRICS_DATA_CENTER:
        return {'error': 'Qualtrics data center not configured'}
    
    base_url = settings.QUALTRICS_API_URL
    endpoint = f"{base_url}/surveys/{survey_id}/responses/{response_id}"
    
    try:
        print(f"=== QUALTRICS API REQUEST DEBUG ===")
        print(f"Endpoint: {endpoint}")
        print(f"Survey ID: {survey_id}")
        print(f"Response ID: {response_id}")
        
        response = requests.get(
            endpoint,
            headers=get_qualtrics_headers()
        )
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_json = response.json()
            print(f"Response JSON keys: {list(response_json.keys()) if isinstance(response_json, dict) else 'Not a dict'}")
            print(f"Full Response JSON: {json.dumps(response_json, indent=2, default=str)}")
            print(f"=== END QUALTRICS API REQUEST DEBUG ===")
            
            return {
                'success': True,
                'data': response_json
            }
        else:
            print(f"Error Response: {response.text}")
            print(f"=== END QUALTRICS API REQUEST DEBUG ===")
            return {
                'error': f'Failed to fetch response: {response.status_code}',
                'details': response.text
            }
    
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'error': f'Unexpected error: {str(e)}'
        }

