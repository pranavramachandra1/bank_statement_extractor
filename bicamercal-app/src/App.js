import React from 'react';
import './App.css';
import PDFUploadForm from './components/PDFUploadForm';

function App() {
  return (
    <div className="App">
      <h1>PDF Bank Account Extractor</h1>
      <PDFUploadForm />
    </div>
  );
}

export default App;