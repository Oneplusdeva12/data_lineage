import React, { useState } from 'react';
import { queryLineage } from '../api';

function QueryForm() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async () => {
    try {
      const res = await queryLineage(query);
      setResponse(res.data.answer);
    } catch (error) {
      setResponse("Error generating lineage.");
    }
  };

  return (
    <div>
      <h2>Ask a Data Lineage Question</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
      />
      <button onClick={handleSubmit}>Submit</button>
      <p><strong>Response:</strong> {response}</p>
    </div>
  );
}

export default QueryForm;