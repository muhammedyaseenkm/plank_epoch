import React, { useState, useEffect } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';

const BASE_URL = process.env.REACT_APP_BASE_URL || 'http://127.0.0.1:5003';

const FetchFileNames = () => {
  const [fileNames, setFileNames] = useState([]);
  const [fetchDataEnabled, setFetchDataEnabled] = useState(false);
  const [fileContent, setFileContent] = useState(null);


  // Auto Render the file Name in the scree
  useEffect(() => {
    const fetchData = async () => {
      try { const response = await axios.get(`${BASE_URL}/file_list`);  setFileNames(response.data)  } 
      catch (error) {  console.error('Error fetching file list:', error)    }
    };

    if (fetchDataEnabled) { fetchData();  } else { setFileNames([]);    }
  }, [fetchDataEnabled]);



  // Making File Name Clickable to view  item Content
  const handleFileNameClick = async (fileName) => {
    try {
      const response = await axios.get(`${BASE_URL}/file_content/${fileName}`, { responseType: 'arraybuffer' })
      const data = new Uint8Array(response.data)
      const workbook = XLSX.read(data, { type: 'array' })
      const jsonData = {};

      workbook.SheetNames.forEach((sheetName) => {
        const sheet = workbook.Sheets[sheetName];
        jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
      });

      setFileContent(jsonData); 
    } 
    catch (error) {console.error('Error fetching file content:', error)   }
  };

  return (
    <div>
      <div>
        <label>
          Enable File Fetching:
          <input
            type="checkbox"
            checked={fetchDataEnabled}
            onChange={(e) => setFetchDataEnabled(e.target.checked)}
          />
        </label>
      </div>
      {fetchDataEnabled ? (
        <>
          {fileNames.map((fileName, index) => (
            <div key={index}>
              <a href={`${BASE_URL}/${fileName}`} target="_blank" rel="noopener noreferrer">
                {/* Replaced div with span for better semantic */}
                <span>{fileName}</span>
              </a>
              {/* Changed to button element */}
              <button onClick={() => handleFileNameClick(fileName)} style={{ marginLeft: '10px', cursor: 'pointer' }}>
                (Open internally)
              </button>
            </div>
          ))}
          {fileContent && (
            <div>
              <h2>Fetched File Content</h2>
              {Object.keys(fileContent).map(sheetName => (
                <div key={sheetName}>
                  <h3>{sheetName}</h3>
                  <pre>{JSON.stringify(fileContent[sheetName], null, 2)}</pre>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <div>Fetched data is disabled</div>
      )}
    </div>
  );
};

export default FetchFileNames;
