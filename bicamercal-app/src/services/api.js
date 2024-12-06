import axios from 'axios';

const API_URL = 'http://localhost:3000'; // Flask backend URL

export const processPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post('/process-pdf', formData, {
    responseType: 'blob', // to receive binary data
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  
  // Create a Blob from the response data assuming it's a ZIP file
  const fileBlob = new Blob([response.data], { type: 'application/zip' });
  
  // Generate a Blob URL for the file
  const downloadUrl = URL.createObjectURL(fileBlob);
  
  // Now you have a URL that you can set as the `href` of a link
  return downloadUrl;
};