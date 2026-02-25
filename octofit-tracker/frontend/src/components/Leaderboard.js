import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [leaders, setLeaders] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = `https://${codespace}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Fetching Leaderboard from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaders(results);
        console.log('Fetched Leaderboard:', results);
      })
      .catch(err => console.error('Error fetching leaderboard:', err));
  }, [endpoint]);

  // Always show Username, Team, and Total Calories, plus any extra columns
  const baseColumns = ['username', 'team', 'total_calories'];
  const extraColumns = leaders.length > 0 ? Object.keys(leaders[0]).filter(key => !baseColumns.includes(key)) : [];
  const columns = [...baseColumns, ...extraColumns];

  function getTeamName(team) {
    if (!team) return 'N/A';
    if (typeof team === 'string') return team;
    if (typeof team === 'object') {
      if (team.name) return team.name;
      if (team.title) return team.title;
      return JSON.stringify(team);
    }
    return 'N/A';
  }

  function getTotalCalories(leader) {
    if (leader.total_calories !== undefined) return leader.total_calories;
    // Try to sum calories from activities if present
    if (Array.isArray(leader.activities)) {
      return leader.activities.reduce((sum, act) => sum + (act.calories || 0), 0);
    }
    return 0;
  }

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <h2 className="card-title mb-4 text-success">Leaderboard</h2>
        <div className="table-responsive">
          <table className="table table-striped table-bordered align-middle">
            <thead className="table-light">
              <tr>
                {columns.map((key) => (
                  <th key={key}>{key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {leaders.map((leader, idx) => (
                <tr key={leader.id || idx}>
                  {columns.map((key, i) => {
                    if (key === 'team') {
                      return <td key={i}>{getTeamName(leader.team)}</td>;
                    }
                    if (key === 'total_calories') {
                      return <td key={i}>{getTotalCalories(leader)}</td>;
                    }
                    return <td key={i}>{leader[key] !== undefined ? (typeof leader[key] === 'object' ? JSON.stringify(leader[key]) : leader[key]) : ''}</td>;
                  })}
                </tr>
              ))}
            </tbody>
          </table>
          {leaders.length === 0 && <div className="text-muted">No leaderboard data found.</div>}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
