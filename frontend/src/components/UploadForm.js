import React from 'react';
import { uploadDocument } from '../api';

function UploadForm() {
  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "text/plain",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];
    if (!allowedTypes.includes(file.type)) {
      alert("Only PDF, DOCX, and TXT files are supported.");
      return;
    }

    try {
      await uploadDocument(file);
      alert("File uploaded and processed successfully.");
    } catch (error) {
      alert("Upload failed.");
    }
  };

  return (
    <div>
      <h2>Upload ETL Spec</h2>
      <input type="file" accept=".pdf,.txt,.docx" onChange={handleUpload} />
    </div>
  );
}

export default UploadForm;
