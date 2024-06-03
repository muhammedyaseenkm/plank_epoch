// src/components/FileList.js
import React from 'react';

const FileList = ({ fileData, onImageClick }) => {
  return (
    <div className="file-container">
      {fileData.map((file, index) => (
        <div key={index} className="file-item">
          <p>File Name: {file.name}</p>
          <img
            src={file.images[0]} // Assuming file.images contains the URLs of images
            alt={`Image ${index}`}
            onClick={() => onImageClick(file.images[0])} // Pass the clicked image URL to onImageClick
          />
        </div>
      ))}
    </div>
  );
};

export default FileList;
