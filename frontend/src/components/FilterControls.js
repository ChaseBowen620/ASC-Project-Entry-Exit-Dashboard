import React, { useState, useEffect } from 'react';
import './FilterControls.css';

const FilterControls = ({ onFiltersChange, availableData }) => {
  const [filters, setFilters] = useState({
    mentor: '',
    topic: '',
    projectName: '',
    startDate: '',
    endDate: ''
  });

  const [showFilters, setShowFilters] = useState(false);

  // Update parent component when filters change
  useEffect(() => {
    onFiltersChange(filters);
  }, [filters, onFiltersChange]);

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const clearAllFilters = () => {
    setFilters({
      mentor: '',
      topic: '',
      projectName: '',
      startDate: '',
      endDate: ''
    });
  };

  const hasActiveFilters = Object.values(filters).some(value => value !== '');

  // Helper function to display mentor names nicely
  const getMentorDisplayName = (mentor) => {
    // If it's a number (1-14), show as "Mentor #X"
    if (/^\d+$/.test(mentor)) {
      return `Mentor #${mentor}`;
    }
    // If it's a custom name, show as is
    return mentor;
  };

  // Get unique values for dropdowns and sort them alphabetically
  const uniqueMentors = (availableData?.mentors || []).sort();
  const uniqueTopics = (availableData?.topics || []).sort();
  const uniqueProjects = (availableData?.projects || []).sort();

  return (
    <div className="filter-controls">
      <div className="filter-header">
        <button 
          className="filter-toggle-btn"
          onClick={() => setShowFilters(!showFilters)}
        >
          <span className="filter-icon">🔍</span>
          Filters {hasActiveFilters && <span className="active-indicator">●</span>}
        </button>
        {hasActiveFilters && (
          <button className="clear-filters-btn" onClick={clearAllFilters}>
            Clear All
          </button>
        )}
      </div>

      {showFilters && (
        <div className="filter-panel">
          <div className="filter-grid">
            {/* Mentor Filter */}
            <div className="filter-group">
              <label htmlFor="mentor-filter">Mentor:</label>
              <select
                id="mentor-filter"
                value={filters.mentor}
                onChange={(e) => handleFilterChange('mentor', e.target.value)}
                className="filter-select"
              >
                <option value="">All Mentors</option>
                {uniqueMentors.map(mentor => (
                  <option key={mentor} value={mentor}>{getMentorDisplayName(mentor)}</option>
                ))}
              </select>
            </div>

            {/* Topic Filter */}
            <div className="filter-group">
              <label htmlFor="topic-filter">Topic:</label>
              <select
                id="topic-filter"
                value={filters.topic}
                onChange={(e) => handleFilterChange('topic', e.target.value)}
                className="filter-select"
              >
                <option value="">All Topics</option>
                {uniqueTopics.map(topic => (
                  <option key={topic} value={topic}>{topic}</option>
                ))}
              </select>
            </div>

            {/* Project Name Filter */}
            <div className="filter-group">
              <label htmlFor="project-filter">Project Name:</label>
              <select
                id="project-filter"
                value={filters.projectName}
                onChange={(e) => handleFilterChange('projectName', e.target.value)}
                className="filter-select"
              >
                <option value="">All Projects</option>
                {uniqueProjects.map(project => (
                  <option key={project} value={project}>{project}</option>
                ))}
              </select>
            </div>

            {/* Date Range Filter */}
            <div className="filter-group date-range">
              <label>Date Range:</label>
              <div className="date-inputs">
                <input
                  type="date"
                  value={filters.startDate}
                  onChange={(e) => handleFilterChange('startDate', e.target.value)}
                  className="filter-date"
                  placeholder="Start Date"
                />
                <span className="date-separator">to</span>
                <input
                  type="date"
                  value={filters.endDate}
                  onChange={(e) => handleFilterChange('endDate', e.target.value)}
                  className="filter-date"
                  placeholder="End Date"
                />
              </div>
            </div>
          </div>

          {/* Active Filters Display */}
          {hasActiveFilters && (
            <div className="active-filters">
              <span className="active-filters-label">Active filters:</span>
              {filters.mentor && (
                <span className="active-filter-tag">
                  Mentor: {getMentorDisplayName(filters.mentor)} 
                  <button onClick={() => handleFilterChange('mentor', '')}>×</button>
                </span>
              )}
              {filters.topic && (
                <span className="active-filter-tag">
                  Topic: {filters.topic} 
                  <button onClick={() => handleFilterChange('topic', '')}>×</button>
                </span>
              )}
              {filters.projectName && (
                <span className="active-filter-tag">
                  Project: {filters.projectName} 
                  <button onClick={() => handleFilterChange('projectName', '')}>×</button>
                </span>
              )}
              {(filters.startDate || filters.endDate) && (
                <span className="active-filter-tag">
                  Date: {filters.startDate || 'Any'} to {filters.endDate || 'Any'} 
                  <button onClick={() => {
                    handleFilterChange('startDate', '');
                    handleFilterChange('endDate', '');
                  }}>×</button>
                </span>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FilterControls;
