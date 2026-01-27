import React, { useState } from 'react';
import axios from 'axios';
import './SubmissionsList.css';

// Configure API base via env; falls back to relative '/api' for proxy/rewrites
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || '/api';

function SubmissionsList({ submissions, onUpdate }) {
  const [editingId, setEditingId] = useState(null);
  const [editingField, setEditingField] = useState(null); // 'project_title' or 'project_mentor'
  const [editingValue, setEditingValue] = useState('');
  const [saving, setSaving] = useState(false);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (e) {
      return dateString;
    }
  };

  const handleEdit = (submission, field) => {
    setEditingId(submission.id);
    setEditingField(field);
    setEditingValue(field === 'project_title' ? (submission.project_title || '') : (submission.project_mentor || ''));
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditingField(null);
    setEditingValue('');
  };

  const handleSave = async (submissionId) => {
    if (saving || !editingField) return;
    
    setSaving(true);
    try {
      const updateData = { [editingField]: editingValue };
      await axios.patch(
        `${API_BASE_URL}/responses/${submissionId}/`,
        updateData,
        {
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      
      // Notify parent component to refresh data
      if (onUpdate) {
        onUpdate();
      }
      
      setEditingId(null);
      setEditingField(null);
      setEditingValue('');
    } catch (error) {
      console.error(`Error updating ${editingField}:`, error);
      const fieldName = editingField === 'project_title' ? 'project name' : 'mentor name';
      alert(`Failed to update ${fieldName}. Please try again.`);
    } finally {
      setSaving(false);
    }
  };

  const handleKeyPress = (e, submissionId) => {
    if (e.key === 'Enter') {
      handleSave(submissionId);
    } else if (e.key === 'Escape') {
      handleCancel();
    }
  };

  if (!submissions || submissions.length === 0) {
    return (
      <div className="submissions-list-container">
        <h2>All Submissions</h2>
        <p className="no-submissions">No submissions found.</p>
      </div>
    );
  }

  // Sort submissions by recorded_date (most recent first)
  const sortedSubmissions = [...submissions].sort((a, b) => {
    const dateA = a.recorded_date ? new Date(a.recorded_date) : new Date(0);
    const dateB = b.recorded_date ? new Date(b.recorded_date) : new Date(0);
    return dateB - dateA; // Descending order (newest first)
  });

  return (
    <div className="submissions-list-container">
      <h2>All Submissions</h2>
      <div className="submissions-table-wrapper">
        <table className="submissions-table">
          <thead>
            <tr>
              <th>Submission Date</th>
              <th>Project Name</th>
              <th>Mentor</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedSubmissions.map((submission) => {
              const isEditingProject = editingId === submission.id && editingField === 'project_title';
              const isEditingMentor = editingId === submission.id && editingField === 'project_mentor';
              const isEditing = isEditingProject || isEditingMentor;
              
              return (
                <tr key={submission.id}>
                  <td>{formatDate(submission.recorded_date)}</td>
                  <td>
                    {isEditingProject ? (
                      <input
                        type="text"
                        value={editingValue}
                        onChange={(e) => setEditingValue(e.target.value)}
                        onKeyDown={(e) => handleKeyPress(e, submission.id)}
                        className="edit-input"
                        autoFocus
                        disabled={saving}
                      />
                    ) : (
                      <span className="field-display">
                        {submission.project_title || 'N/A'}
                      </span>
                    )}
                  </td>
                  <td>
                    {isEditingMentor ? (
                      <input
                        type="text"
                        value={editingValue}
                        onChange={(e) => setEditingValue(e.target.value)}
                        onKeyDown={(e) => handleKeyPress(e, submission.id)}
                        className="edit-input"
                        autoFocus
                        disabled={saving}
                      />
                    ) : (
                      <span className="field-display">
                        {submission.project_mentor || 'N/A'}
                      </span>
                    )}
                  </td>
                  <td>
                    {isEditing ? (
                      <div className="edit-actions">
                        <button
                          onClick={() => handleSave(submission.id)}
                          disabled={saving}
                          className="save-btn"
                          title="Save (Enter)"
                        >
                          {saving ? 'Saving...' : 'Save'}
                        </button>
                        <button
                          onClick={handleCancel}
                          disabled={saving}
                          className="cancel-btn"
                          title="Cancel (Esc)"
                        >
                          Cancel
                        </button>
                      </div>
                    ) : (
                      <div className="action-buttons">
                        <button
                          onClick={() => handleEdit(submission, 'project_title')}
                          className="edit-btn"
                          title="Click to rename project"
                        >
                          Edit Project
                        </button>
                        <button
                          onClick={() => handleEdit(submission, 'project_mentor')}
                          className="edit-btn"
                          title="Click to rename mentor"
                        >
                          Edit Mentor
                        </button>
                      </div>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default SubmissionsList;

