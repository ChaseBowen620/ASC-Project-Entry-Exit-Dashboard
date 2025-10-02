import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import SummaryNumbers from './components/SummaryNumbers';
import FilterControls from './components/FilterControls';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [allResponses, setAllResponses] = useState([]);
  const [filteredData, setFilteredData] = useState({
    stats: null,
    analytics: null
  });
  const [availableData, setAvailableData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});

  // Helper function to get mentor name from response
  const getMentorName = (response) => {
    // Check Q2.3 (starting survey) or Q3.3 (ending survey)
    const mentorChoice = response.mentor_choice;
    
    // Mentor mapping based on Mentor Values.txt
    const mentorNames = {
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
    };
    
    if (mentorChoice === 15) {
      // If choice is 15 (Other), use the text input from Q2.3.a or Q3.3.a
      return response.mentor_name || 'Other';
    } else if (mentorChoice >= 1 && mentorChoice <= 14) {
      // Return the actual mentor name for choices 1-14
      return mentorNames[mentorChoice] || '';
    }
    
    return '';
  };

  // Helper function to get topic name from response
  const getTopicName = (response) => {
    // Check Q2.6 (starting survey) or Q3.8 (ending survey)
    const topicValue = response.topics_working_on || response.topics_worked_on;
    
    const topicMapping = {
      1: 'Data Engineering and Visualization',
      2: 'Business Intelligence and Analytics', 
      3: 'Machine Learning and AI',
      4: 'Predictive and Advanced Analytics',
      5: 'Software Development and Web Design'
    };
    
    return topicMapping[topicValue] || '';
  };

  // Load all data once on component mount
  const fetchAllData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // First test if API is working
      const testResponse = await axios.get(`${API_BASE_URL}/test/`);
      console.log('API test successful:', testResponse.data);
      
      const responsesResponse = await axios.get(`${API_BASE_URL}/responses/`);
      
      const responses = responsesResponse.data.results || responsesResponse.data;
      setAllResponses(responses);
      
      // Calculate available data from the responses
      const responseMentors = [...new Set(responses.map(r => getMentorName(r)).filter(Boolean))];
      const responseTopics = [...new Set(responses.map(r => getTopicName(r)).filter(Boolean))];
      const projects = [...new Set(responses.map(r => r.project_title).filter(Boolean))].sort();
      
      // Always include all mentor options (actual mentor names + any custom names from data)
      const mentorNames = {
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
        14: 'Brinley Zabriskie'
      };
      
      const allMentorOptions = Object.values(mentorNames);
      // Add any custom mentor names from the data (for "Other" selections)
      const customMentors = responseMentors.filter(mentor => !Object.values(mentorNames).includes(mentor));
      allMentorOptions.push(...customMentors);
      
      // Always include all topic options
      const allTopicOptions = [
        'Data Engineering and Visualization',
        'Business Intelligence and Analytics',
        'Machine Learning and AI',
        'Predictive and Advanced Analytics',
        'Software Development and Web Design'
      ];
      
      // Set initial available data (will be updated dynamically based on filters)
      setAvailableData({
        mentors: allMentorOptions,
        topics: allTopicOptions,
        projects
      });
    } catch (err) {
      const errorMessage = err.response?.data?.error || err.message || 'Unknown error';
      setError(`Failed to fetch dashboard data: ${errorMessage}. Make sure the Django backend is running on http://localhost:8000`);
      console.error('Error fetching data:', err);
      console.error('Error response:', err.response?.data);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load data once on mount
  useEffect(() => {
    fetchAllData();
  }, [fetchAllData]);

  // Client-side filtering function
  const applyFilters = useCallback((responses, filters) => {
    return responses.filter(response => {
      // Mentor filter
      if (filters.mentor) {
        const mentorName = getMentorName(response);
        const mentorMatch = mentorName.toLowerCase().includes(filters.mentor.toLowerCase());
        if (!mentorMatch) return false;
      }

      // Project name filter
      if (filters.projectName) {
        const projectMatch = response.project_title?.toLowerCase().includes(filters.projectName.toLowerCase());
        if (!projectMatch) return false;
      }

      // Topic filter
      if (filters.topic) {
        const topicName = getTopicName(response);
        const topicMatch = topicName === filters.topic;
        if (!topicMatch) return false;
      }

      // Date range filter
      if (filters.startDate) {
        const responseDate = new Date(response.end_date);
        const startDate = new Date(filters.startDate);
        if (responseDate < startDate) return false;
      }

      if (filters.endDate) {
        const responseDate = new Date(response.end_date);
        const endDate = new Date(filters.endDate);
        if (responseDate > endDate) return false;
      }

      return true;
    });
  }, []);

  // Calculate stats and analytics from filtered data
  const calculateFilteredData = useCallback((responses) => {
    const total_responses = responses.length;
    const starting_responses = responses.filter(r => r.survey_type === 1).length;
    const ending_responses = responses.filter(r => r.survey_type === 2).length;

    // Calculate average ratings for ending surveys
    const ending_surveys = responses.filter(r => r.survey_type === 2);
    const avg_ratings = {};
    
    const rating_fields = [
      'rating_onboarding', 'rating_initiation', 'rating_mentorship',
      'rating_team', 'rating_communications', 'rating_expectations',
      'rating_sponsor', 'rating_workload'
    ];

    rating_fields.forEach(field => {
      const values = ending_surveys
        .map(r => r[field])
        .filter(val => val !== null && val !== undefined);
      
      if (values.length > 0) {
        avg_ratings[field] = Math.round((values.reduce((sum, val) => sum + val, 0) / values.length) * 100) / 100;
      }
    });

    // Average recommendation score
    const recommend_scores = ending_surveys
      .map(r => r.recommend_asc)
      .filter(val => val !== null && val !== undefined);
    
    const avg_recommendation = recommend_scores.length > 0 
      ? Math.round((recommend_scores.reduce((sum, val) => sum + val, 0) / recommend_scores.length) * 100) / 100
      : null;

    const completion_rate = starting_responses > 0 
      ? Math.round((ending_responses / starting_responses * 100) * 100) / 100 
      : 0;

    // Analytics data
    const topics_starting = responses
      .filter(r => r.survey_type === 1 && r.topics_working_on)
      .map(r => r.topics_working_on);
    
    const topics_ending = responses
      .filter(r => r.survey_type === 2 && r.topics_worked_on)
      .map(r => r.topics_worked_on);
    
    const confidence_levels = responses
      .filter(r => r.survey_type === 2 && r.confidence_job_placement)
      .map(r => r.confidence_job_placement);
    
    const hard_skills_improvement = responses
      .filter(r => r.survey_type === 2 && r.hard_skills_improved)
      .map(r => r.hard_skills_improved);
    
    const soft_skills_improvement = responses
      .filter(r => r.survey_type === 2 && r.soft_skills_improved)
      .map(r => r.soft_skills_improved);

    return {
      stats: {
        total_responses,
        starting_responses,
        ending_responses,
        average_ratings: avg_ratings,
        average_recommendation: avg_recommendation,
        completion_rate
      },
      analytics: {
        topics_starting,
        topics_ending,
        confidence_levels,
        hard_skills_improvement,
        soft_skills_improvement
      }
    };
  }, []);

  // Calculate available options based on current filters
  const calculateAvailableOptions = useCallback((responses, currentFilters) => {
    // Start with all responses and apply filters one by one to get available options
    let availableResponses = responses;
    
    // Apply mentor filter if present
    if (currentFilters.mentor) {
      availableResponses = availableResponses.filter(response => {
        const mentorName = getMentorName(response);
        return mentorName.toLowerCase().includes(currentFilters.mentor.toLowerCase());
      });
    }
    
    // Apply topic filter if present
    if (currentFilters.topic) {
      availableResponses = availableResponses.filter(response => {
        const topicName = getTopicName(response);
        return topicName === currentFilters.topic;
      });
    }
    
    // Apply date filters if present
    if (currentFilters.startDate) {
      const startDate = new Date(currentFilters.startDate);
      availableResponses = availableResponses.filter(response => {
        const responseDate = new Date(response.end_date);
        return responseDate >= startDate;
      });
    }
    
    if (currentFilters.endDate) {
      const endDate = new Date(currentFilters.endDate);
      availableResponses = availableResponses.filter(response => {
        const responseDate = new Date(response.end_date);
        return responseDate <= endDate;
      });
    }
    
    // Now calculate available options from the filtered responses
    const availableMentors = [...new Set(availableResponses.map(r => getMentorName(r)).filter(Boolean))];
    const availableTopics = [...new Set(availableResponses.map(r => getTopicName(r)).filter(Boolean))];
    const availableProjects = [...new Set(availableResponses.map(r => r.project_title).filter(Boolean))].sort();
    
    return {
      mentors: availableMentors,
      topics: availableTopics,
      projects: availableProjects
    };
  }, [getMentorName, getTopicName]);

  // Update filtered data when filters or all responses change
  useEffect(() => {
    if (allResponses.length > 0) {
      const filtered = applyFilters(allResponses, filters);
      const calculated = calculateFilteredData(filtered);
      setFilteredData(calculated);
      
      // Update available options based on current filters
      const availableOptions = calculateAvailableOptions(allResponses, filters);
      setAvailableData(prevData => ({
        ...prevData,
        ...availableOptions
      }));
    }
  }, [allResponses, filters, applyFilters, calculateFilteredData, calculateAvailableOptions]);

  const handleFiltersChange = (newFilters) => {
    setFilters(newFilters);
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <h2>Loading Dashboard...</h2>
          <p>Make sure the Django backend is running on http://localhost:8000</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={fetchAllData}>Retry</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>ASC Survey Dashboard</h1>
        <div className="stats-overview">
          <div className="stat-item">
            <span className="stat-number">{filteredData.stats?.total_responses || 0}</span>
            <span className="stat-label">Total Responses</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{filteredData.stats?.starting_responses || 0}</span>
            <span className="stat-label">Starting Projects</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{filteredData.stats?.ending_responses || 0}</span>
            <span className="stat-label">Ending Projects</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{filteredData.stats?.completion_rate || 0}%</span>
            <span className="stat-label">Completion Rate</span>
          </div>
        </div>
      </header>

      <main className="app-main">
        <FilterControls 
          onFiltersChange={handleFiltersChange}
          availableData={availableData}
        />
        <SummaryNumbers 
          dashboardStats={filteredData.stats} 
          analytics={filteredData.analytics} 
        />
      </main>
    </div>
  );
}

export default App;
