import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = `https://${codespace}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Fetching Activities from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched Activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, [endpoint]);

  // Helper to format date strings
  function formatDate(val) {
    if (!val) return '';
    // Try to parse ISO or common date formats
    let d = null;
    if (typeof val === 'string' && val.match(/^\d{4}-\d{2}-\d{2}/)) {
      // If string looks like '2024-02-25T14:00:00Z' or similar
      d = new Date(val);
    } else if (typeof val === 'number') {
      d = new Date(val);
    }
    if (d && !isNaN(d)) {
      return d.toLocaleString();
    }
    return val;
  }

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <h2 className="card-title mb-4 text-primary">Activities</h2>
        <div className="table-responsive">
          <table className="table table-striped table-bordered align-middle">
            <thead className="table-light">
              <tr>
                {activities.length > 0 && Object.keys(activities[0]).map((key) => (
                  <th key={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {activities.map((activity, idx) => (
                <tr key={activity.id || idx}>
                  {Object.entries(activity).map(([key, value], i) => (
                    <td key={i}>
                      {key.toLowerCase().includes('date') ? formatDate(value) : (typeof value === 'object' ? JSON.stringify(value) : value)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {activities.length === 0 && <div className="text-muted">No activities found.</div>}
        </div>
      </div>
    </div>
  );
};

export default Activities;
