// src/components/ImageViewer.js
import React from 'react';
import { fetchFirstImage } from './fetchUtils'; // Adjust the import path to '../fileUtils'

const ImageViewer = ({ fileData }) => {
  return (
    <div>
      <p>Image Viewer:</p>
      <div>
        {fileData.map((file, index) => (
          <div key={index}>
            <img src={fetchFirstImage(file)} alt={`Image ${index + 1}`} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageViewer;
