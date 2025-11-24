import React from 'react';
import './ResponseDetailModal.css';

function ResponseDetailModal({ response, isOpen, onClose }) {
  if (!isOpen || !response) return null;

  // Extract Qualtrics response data - handle both Qualtrics API format and database format
  const getResponseValue = (key) => {
    // Check if this is a Qualtrics API response format
    if (response.result && response.result.values) {
      return response.result.values[key] || response.result.values[`${key}_TEXT`] || null;
    }
    // Otherwise assume it's database format
    return response[key] || null;
  };

  const getResponseId = () => {
    if (response.result && response.result.responseId) {
      return response.result.responseId;
    }
    return response.response_id || response.id || 'N/A';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return dateString;
    }
  };

  const formatRating = (value) => {
    if (value === null || value === undefined) return 'N/A';
    const ratings = { 1: 'Poor', 2: 'Neutral/Fair', 3: 'Excellent' };
    return `${value} (${ratings[value] || 'N/A'})`;
  };

  const formatAgreement = (value) => {
    if (value === null || value === undefined) return 'N/A';
    const agreements = {
      1: 'Strongly Disagree',
      2: 'Somewhat Disagree',
      3: 'Neither Agree nor Disagree',
      4: 'Somewhat Agree',
      5: 'Strongly Agree'
    };
    return `${value} (${agreements[value] || 'N/A'})`;
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Complete Response Details</h2>
          <button className="modal-close-btn" onClick={onClose}>&times;</button>
        </div>
        <div className="modal-body">
          <div className="response-section">
            <h3>Basic Information</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>Response ID:</label>
                <span>{getResponseId()}</span>
              </div>
              <div className="detail-item">
                <label>Survey Type:</label>
                <span>{getResponseValue('Q1.1') || response.survey_type_display || (response.survey_type === 2 ? 'Ending Project' : 'Starting Project')}</span>
              </div>
              <div className="detail-item">
                <label>Recorded Date:</label>
                <span>{formatDate(getResponseValue('RecordedDate') || response.recorded_date)}</span>
              </div>
              <div className="detail-item">
                <label>Start Date:</label>
                <span>{formatDate(getResponseValue('StartDate') || response.start_date)}</span>
              </div>
              <div className="detail-item">
                <label>End Date:</label>
                <span>{formatDate(getResponseValue('EndDate') || response.end_date)}</span>
              </div>
              <div className="detail-item">
                <label>Finished:</label>
                <span>{getResponseValue('Finished') || (response.finished ? 'Yes' : 'No')}</span>
              </div>
            </div>
          </div>

          <div className="response-section">
            <h3>Project Information</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>A Number:</label>
                <span>{getResponseValue('Q3.1') || response.a_number || 'N/A'}</span>
              </div>
              <div className="detail-item">
                <label>Project Title:</label>
                <span>{getResponseValue('Q3.2') || response.project_title || 'N/A'}</span>
              </div>
              <div className="detail-item">
                <label>Mentor:</label>
                <span>{getResponseValue('Q3.3') === 'Other' ? (getResponseValue('Q3.3.a') || 'Other') : (getResponseValue('Q3.3') || response.project_mentor || 'N/A')}</span>
              </div>
              <div className="detail-item">
                <label>Topic:</label>
                <span>{getResponseValue('Q3.8') || response.topic || 'N/A'}</span>
              </div>
            </div>
          </div>

          <div className="response-section">
            <h3>Skills & Confidence</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>Hard Skills Improved:</label>
                <span>{getResponseValue('Q3.9') || formatAgreement(response.hard_skills_improved)}</span>
              </div>
              <div className="detail-item">
                <label>Soft Skills Improved:</label>
                <span>{getResponseValue('Q3.10') || formatAgreement(response.soft_skills_improved)}</span>
              </div>
              <div className="detail-item">
                <label>Confidence in Job Placement:</label>
                <span>{getResponseValue('Q3.11') || formatAgreement(response.confidence_job_placement)}</span>
              </div>
            </div>
          </div>

          <div className="response-section">
            <h3>Ratings</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>Onboarding:</label>
                <span>{getResponseValue('Q3.12.a') || formatRating(response.rating_onboarding)}</span>
              </div>
              <div className="detail-item">
                <label>Initiation:</label>
                <span>{getResponseValue('Q3.12.b') || formatRating(response.rating_initiation)}</span>
              </div>
              <div className="detail-item">
                <label>Mentorship:</label>
                <span>{getResponseValue('Q3.12.c') || formatRating(response.rating_mentorship)}</span>
              </div>
              <div className="detail-item">
                <label>Team:</label>
                <span>{getResponseValue('Q3.12.d') || formatRating(response.rating_team)}</span>
              </div>
              <div className="detail-item">
                <label>Communications:</label>
                <span>{getResponseValue('Q3.12.e') || formatRating(response.rating_communications)}</span>
              </div>
              <div className="detail-item">
                <label>Expectations:</label>
                <span>{getResponseValue('Q3.12.f') || formatRating(response.rating_expectations)}</span>
              </div>
              <div className="detail-item">
                <label>Sponsor:</label>
                <span>{getResponseValue('Q3.12.g') || formatRating(response.rating_sponsor)}</span>
              </div>
              <div className="detail-item">
                <label>Workload:</label>
                <span>{getResponseValue('Q3.12.h') || formatRating(response.rating_workload)}</span>
              </div>
            </div>
          </div>

          <div className="response-section">
            <h3>Additional Information</h3>
            <div className="detail-grid">
              <div className="detail-item full-width">
                <label>What Gained/Learned:</label>
                <span className="text-content">{getResponseValue('Q3.5') || response.gained_learned || 'N/A'}</span>
              </div>
              <div className="detail-item full-width">
                <label>What Went Well:</label>
                <span className="text-content">{getResponseValue('Q3.6') || response.what_went_well || 'N/A'}</span>
              </div>
              <div className="detail-item full-width">
                <label>What Could Improve:</label>
                <span className="text-content">{getResponseValue('Q3.7') || response.what_could_improve || 'N/A'}</span>
              </div>
              <div className="detail-item full-width">
                <label>Additional Comments:</label>
                <span className="text-content">{getResponseValue('Q3.14') || response.additional_comments_ending || 'N/A'}</span>
              </div>
              <div className="detail-item">
                <label>Recommend ASC:</label>
                <span>{getResponseValue('Q3.13') || (response.recommend_asc !== null && response.recommend_asc !== undefined ? response.recommend_asc : 'N/A')}</span>
              </div>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="modal-close-button" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}

export default ResponseDetailModal;

