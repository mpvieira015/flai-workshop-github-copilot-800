import React, { useEffect, useState } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = `https://${codespace}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Fetching Users from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setUsers(results);
        console.log('Fetched Users:', results);
      })
      .catch(err => console.error('Error fetching users:', err));
  }, [endpoint]);

  // Always show Name and Username columns, plus any others
  const baseColumns = ['name', 'username'];
  const extraColumns = users.length > 0 ? Object.keys(users[0]).filter(key => !baseColumns.includes(key)) : [];
  const columns = [...baseColumns, ...extraColumns];

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-body">
        <h2 className="card-title mb-4 text-secondary">Users</h2>
        <div className="table-responsive">
          <table className="table table-striped table-bordered align-middle">
            <thead className="table-light">
              <tr>
                {columns.map((key) => (
                  <th key={key}>{key.charAt(0).toUpperCase() + key.slice(1)}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {users.map((user, idx) => (
                <tr key={user.id || idx}>
                  {columns.map((key, i) => (
                    <td key={i}>{user[key] !== undefined ? (typeof user[key] === 'object' ? JSON.stringify(user[key]) : user[key]) : ''}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {users.length === 0 && <div className="text-muted">No users found.</div>}
        </div>
      </div>
    </div>
  );
};

export default Users;
