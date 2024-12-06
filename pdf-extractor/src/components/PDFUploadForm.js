import React, { useState } from 'react';
import { processPDF } from '../services/api';

const PDFUploadForm = () => {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a PDF file.");
      return;
    }

    // Begin loading state
    setIsLoading(true);
    setDownloadUrl(null);

    try {
      const url = await processPDF(file);
      setDownloadUrl(url);
    } catch (error) {
      console.error("Error processing PDF:", error);
    } finally {
      // Stop loading regardless of success or error
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button 
          type="submit" 
          style={{
            backgroundColor: isLoading ? 'red' : '',
            color: isLoading ? 'white' : '',
          }}
        >
          {isLoading ? 'Loading...' : 'Upload and Process'}
        </button>
      </form>
      {!isLoading && downloadUrl && (
        <a href={downloadUrl} download="processed_data.zip">Download Processed File</a>
      )}
    </div>
  );
};

export default PDFUploadForm;