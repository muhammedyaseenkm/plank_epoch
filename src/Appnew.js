import React, { useState, useEffect } from 'react';
import { handleFolderSelection, fetchFirstImage } from './components/fileUpload';
import { fetchImageFromServer } from './imageFetcher';
import { Container, Row, Col, Image, Button } from 'react-bootstrap';

function App() {
  const [fileNames, setFileNames] = useState([]);
  const [imageSrc, setImageSrc] = useState('/get-image');

  const onFolderSelectionChange = (event) => {
    const files = event.target.files;
    handleFolderSelection(files, setFileNames);
  };
  
  const updateImage = () => {
    fetch("/get-image").then(response => {
      setImageSrc('/get-image?' + new Date().getTime());
    });
  };

  useEffect(() => {
    const loadImage = async () => {
      const imageUrl = await fetchImageFromServer();
      if (imageUrl) {
        setImageSrc(imageUrl);
      }
    };
    loadImage();
  }, []);

  return (
    <div className="App">
      <Container>
        <Row>
          <Col>
            <Image src={imageSrc} rounded/>
          </Col>
        </Row>
        <Row>
          <Col>
            <Button onClick={() => updateImage()}>Original</Button>
          </Col>
        </Row>
      </Container>

      <header className="App-header">
        <input
          type="file"
          directory=""
          webkitdirectory=""
          onChange={onFolderSelectionChange}
          multiple
        />
        <p>Selected Files:</p>
        <ul>
          {fileNames.map((name, index) => (
            <li key={index}>{name}</li>
          ))}
        </ul>
        <button onClick={() => fetchFirstImage(setImageSrc)}>Fetch First Image</button>
        <h1>Image from Flask</h1>
        {imageSrc && <img src={imageSrc} alt="First Image" />}
      </header>
      <body>
        <div>
          {imageSrc ? <img src={imageSrc} alt="Flask Image" /> : <p>Loading...</p>}
          <img src="http://localhost:5000/get-image" />
        </div>
        <div>   
           <img src="http://localhost:5000/get-image" />
        </div>
      </body>
    </div>
  );
}

export default App;
