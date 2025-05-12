import React from 'react';
import UploadForm from './components/UploadForm';
import QueryForm from './components/QueryForm';

function App() {
  return (
    <div className="App">
      <h1>Data Lineage RAG Application</h1>
      <UploadForm />
      <QueryForm />
    </div>
  );
}

export default App;