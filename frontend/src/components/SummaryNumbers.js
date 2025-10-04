import React from 'react';
import './SummaryNumbers.css';

const SummaryNumbers = ({ dashboardStats, analytics, allResponses }) => {
  // Helper function to transform values to -1 to 1 scale
  const transformToScale = (value, originalMin, originalMax) => {
    if (value === null || value === undefined) return 0;
    return ((value - originalMin) / (originalMax - originalMin)) * 2 - 1;
  };

  // Helper function to get color based on transformed value
  const getColor = (transformedValue) => {
    if (transformedValue === 0) return '#2c3e50'; // Dark blue-gray at 0
    
    if (transformedValue > 0) {
      // Muted green gradient for positive values
      const intensity = Math.abs(transformedValue);
      // Use a softer green palette: from dark green to lighter green
      const baseGreen = 100; // Base green value
      const maxGreen = 180; // Maximum green value (less harsh)
      const green = Math.round(baseGreen + (maxGreen - baseGreen) * intensity);
      return `rgb(50, ${green}, 80)`;
    } else {
      // Muted red gradient for negative values
      const intensity = Math.abs(transformedValue);
      // Use a softer red palette: from dark red to lighter red
      const baseRed = 100; // Base red value
      const maxRed = 180; // Maximum red value (less harsh)
      const red = Math.round(baseRed + (maxRed - baseRed) * intensity);
      return `rgb(${red}, 50, 50)`;
    }
  };

  // Helper function to format the display value
  const formatValue = (value, originalMin, originalMax) => {
    if (value === null || value === undefined) return 'N/A';
    const transformed = transformToScale(value, originalMin, originalMax);
    return transformed.toFixed(2);
  };

  // Get average values from analytics data
  const getAverageValue = (fieldName) => {
    if (!analytics || !analytics[fieldName] || analytics[fieldName].length === 0) {
      return null;
    }
    const values = analytics[fieldName];
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  };

  // Normalize value from original scale to -1 to 1
  const normalizeValue = (value, minVal = 1, maxVal = 5) => {
    if (value === null || value === undefined) return null;
    return 2 * (value - minVal) / (maxVal - minVal) - 1;
  };

  // Get overall average from all responses (not just filtered ones) and normalize it
  const getOverallAverage = (fieldName, minVal = 1, maxVal = 5) => {
    if (!allResponses || allResponses.length === 0) {
      return null;
    }
    
    // For rating fields, get from ending surveys only
    const endingSurveys = allResponses.filter(r => r.survey_type === 2);
    const values = endingSurveys
      .map(r => r[fieldName])
      .filter(val => val !== null && val !== undefined);
    
    if (values.length === 0) return null;
    const average = values.reduce((sum, val) => sum + val, 0) / values.length;
    return normalizeValue(average, minVal, maxVal);
  };

  // Calculate averages for each metric
  const hardSkillsAvg = getAverageValue('hard_skills_improvement');
  const softSkillsAvg = getAverageValue('soft_skills_improvement');
  const confidenceAvg = getAverageValue('confidence_levels');

  // Get overall averages for the first three metrics (1-5 scale)
  const overallHardSkills = getOverallAverage('hard_skills_improved', 1, 5);
  const overallSoftSkills = getOverallAverage('soft_skills_improved', 1, 5);
  const overallConfidence = getOverallAverage('confidence_job_placement', 1, 5);
  
  // Get rating averages from dashboard stats (filtered data)
  const ratingOnboarding = dashboardStats?.average_ratings?.rating_onboarding;
  const ratingInitiation = dashboardStats?.average_ratings?.rating_initiation;
  const ratingMentorship = dashboardStats?.average_ratings?.rating_mentorship;
  const ratingTeam = dashboardStats?.average_ratings?.rating_team;
  const ratingCommunications = dashboardStats?.average_ratings?.rating_communications;
  const ratingExpectations = dashboardStats?.average_ratings?.rating_expectations;
  const ratingSponsor = dashboardStats?.average_ratings?.rating_sponsor;
  const ratingWorkload = dashboardStats?.average_ratings?.rating_workload;

  // Get overall averages for all responses (1-3 scale for ratings)
  const overallRatingOnboarding = getOverallAverage('rating_onboarding', 1, 3);
  const overallRatingInitiation = getOverallAverage('rating_initiation', 1, 3);
  const overallRatingMentorship = getOverallAverage('rating_mentorship', 1, 3);
  const overallRatingTeam = getOverallAverage('rating_team', 1, 3);
  const overallRatingCommunications = getOverallAverage('rating_communications', 1, 3);
  const overallRatingExpectations = getOverallAverage('rating_expectations', 1, 3);
  const overallRatingSponsor = getOverallAverage('rating_sponsor', 1, 3);
  const overallRatingWorkload = getOverallAverage('rating_workload', 1, 3);

  const summaryItems = [
    {
      title: "Hard Skills Improved",
      value: hardSkillsAvg,
      overallValue: overallHardSkills,
      originalMin: 1,
      originalMax: 5,
      description: "Q3.9 - My hard skills improved in the areas where I was involved"
    },
    {
      title: "Soft Skills Improved", 
      value: softSkillsAvg,
      overallValue: overallSoftSkills,
      originalMin: 1,
      originalMax: 5,
      description: "Q3.10 - This project helped improve my soft skills"
    },
    {
      title: "Confidence in Job Placement",
      value: confidenceAvg,
      overallValue: overallConfidence,
      originalMin: 1,
      originalMax: 5,
      description: "Q3.11 - This project has increased my confidence in securing a job"
    },
    {
      title: "ASC Onboarding",
      value: ratingOnboarding,
      overallValue: overallRatingOnboarding,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_1 - Rating for ASC Onboarding experience"
    },
    {
      title: "Project Initiation",
      value: ratingInitiation,
      overallValue: overallRatingInitiation,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_2 - Rating for Project Initiation experience"
    },
    {
      title: "Project Mentorship",
      value: ratingMentorship,
      overallValue: overallRatingMentorship,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_3 - Rating for Project Mentorship experience"
    },
    {
      title: "Project Team",
      value: ratingTeam,
      overallValue: overallRatingTeam,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_4 - Rating for Project Team experience"
    },
    {
      title: "Project Communications",
      value: ratingCommunications,
      overallValue: overallRatingCommunications,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_5 - Rating for Project Communications experience"
    },
    {
      title: "Expectations",
      value: ratingExpectations,
      overallValue: overallRatingExpectations,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_6 - Rating for Expectations experience"
    },
    {
      title: "Project Sponsor/Contact",
      value: ratingSponsor,
      overallValue: overallRatingSponsor,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_7 - Rating for Project Sponsor/Contact experience"
    },
    {
      title: "Workload",
      value: ratingWorkload,
      overallValue: overallRatingWorkload,
      originalMin: 1,
      originalMax: 3,
      description: "Q3.12_8 - Rating for Workload experience"
    }
  ];

  return (
    <div className="summary-numbers">
      <h2>Survey Summary Metrics</h2>
      <p className="summary-description">
        Values transformed to -1 to 1 scale. Black = 0, Red = negative, Green = positive
      </p>
      
      <div className="summary-grid">
        {summaryItems.map((item, index) => {
          const transformedValue = transformToScale(item.value, item.originalMin, item.originalMax);
          const backgroundColor = getColor(transformedValue);
          const displayValue = formatValue(item.value, item.originalMin, item.originalMax);
          
          return (
            <div 
              key={index} 
              className="summary-square"
              style={{ backgroundColor }}
              title={item.description}
            >
              <div className="summary-content">
                <h3 className="summary-title">{item.title}</h3>
                <div className="summary-value">{displayValue}</div>
                <div className="summary-original">
                  Average: {item.overallValue !== null && item.overallValue !== undefined ? item.overallValue.toFixed(2) : 'N/A'}
                </div>
              </div>
            </div>
          );
        })}
      </div>
      
      <div className="legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: getColor(-1) }}></div>
          <span>Negative (-1)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: getColor(0) }}></div>
          <span>Neutral (0)</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: getColor(1) }}></div>
          <span>Positive (+1)</span>
        </div>
      </div>
    </div>
  );
};

export default SummaryNumbers;
