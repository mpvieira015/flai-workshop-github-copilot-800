import React, { useEffect, useState } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = `https://${codespace}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Fetching Teams from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setTeams(results);
        console.log('Fetched Teams:', results);
      })
      .catch(err => console.error('Error fetching teams:', err));
  }, [endpoint]);

  // Always show Name, Members, and any extra columns
  const baseColumns = ['name', 'members'];
  const extraColumns = teams.length > 0 ? Object.keys(teams[0]).filter(key => !baseColumns.includes(key)) : [];
  const columns = [...baseColumns, ...extraColumns];

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <h2 className="card-title mb-4 text-info">Teams</h2>
        <div className="table-responsive">
          <table className="table table-striped table-bordered align-middle">
            <thead className="table-light">
              <tr>
                {columns.map((key) => (
                  <th key={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</th>
                ))}
                <th key="memberCount"># Members</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((team, idx) => (
                <tr key={team.id || idx}>
                  {columns.map((key, i) => (
                    <td key={i}>
                      {key === 'members' && Array.isArray(team[key])
                        ? JSON.stringify(team[key])
                        : team[key] !== undefined
                          ? (typeof team[key] === 'object' ? JSON.stringify(team[key]) : team[key])
                          : ''}
                    </td>
                  ))}
                  <td key="memberCount">
                    {Array.isArray(team.members)
                      ? team.members.length
                      : (team.members && typeof team.members === 'object' && team.members.length !== undefined)
                        ? team.members.length
                        : 0}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {teams.length === 0 && <div className="text-muted">No teams found.</div>}
        </div>
      </div>
    </div>
  );
};

export default Teams;
