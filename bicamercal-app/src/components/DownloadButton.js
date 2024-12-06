import React from 'react';

const DownloadButton = ({ url }) => {
  return (
    <div>
      <a href={url} download="processed_file.pdf">
        <button>Download Processed File</button>
      </a>
    </div>
  );
};

export default DownloadButton;