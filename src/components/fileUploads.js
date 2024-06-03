import React, { useState } from 'react';
import './App.css';

const CHUNK_SIZE = 1024 * 1024 * 5; // 5 MB

function App() {
  const [fileNames, setFileNames] = useState([]);
  const [imageSrc, setImageSrc] = useState('');

  const handleChunkUpload = async (file) => {
    const chunks = [];
    let start = 0;

    while (start < file.size) {
      chunks.push(file.slice(start, start + CHUNK_SIZE));
      start += CHUNK_SIZE;
    }

    const requests = chunks.map(async (chunk, index) => {
      const formData = new FormData();
      formData.append('fileChunk', chunk, `${file.name}.${index}`);

      try {
        const response = await fetch('http://127.0.0.1:5000/api/upload-images', {
          method: 'POST',
          body: formData,
        });
        if (!response.ok) {
          throw new Error('Failed to upload file chunk');
        }
        console.log(`Chunk ${index} uploaded successfully`);
      } catch (error) {
        console.error('Error uploading chunk:', error);
      }
    });

    await Promise.all(requests);
  };

  const handleFolderSelection = async (event) => {
    const files = event.target.files;
    const names = [];

    for (let i = 0; i < files.length; i++) {
      names.push(files[i].name);
      await handleChunkUpload(files[i]); // Upload each file in chunks
    }

    setFileNames(names);
  };

  const fetchFirstImage = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/first-image');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const blob = await response.blob();
      const imgUrl = URL.createObjectURL(blob);
      setImageSrc(imgUrl);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <input
          type="file"
          directory=""
          webkitdirectory=""
          onChange={handleFolderSelection}
          multiple
        />
        <p>Selected Files:</p>
        <ul>
          {fileNames.map((name, index) => (
            <li key={index}>{name}</li>
          ))}
        </ul>
        <button onClick={fetchFirstImage}>Fetch First Image</button>
        <h1>Image from Flask</h1>
        {imageSrc && <img src={imageSrc} alt="First Image" />}
      </header>
    </div>
  );
}

export default App;
