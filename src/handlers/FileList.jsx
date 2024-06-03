import React, { useState, useCallback } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';

const BASE_URL = 'http://127.0.0.1:5003';

const FileList = () => {
  const [fileNames, setFileNames] = useState([])
  const [fileData, setFileData] = useState(null)
  const [excelUrl, setExcelUrl] = useState(null)
  const [loading, setLoading] = useState(false) 
  const [selectedFileName, setSelectedFileName] = useState(null); // New state to hold the selected file name

  // List File
  const fetchFileNames = useCallback(async () => {
    try {     setLoading(true);
              const response = await axios.get(`${BASE_URL}/file_list`)
              setFileNames(response.data)
        } 
    catch (error) { console.error('Error fetching file list:', error) }
    finally {setLoading(false)}
  }, [BASE_URL]);   // Execute the effect whenever BASE_URL changes


// Fetch File Content
// const fetchFileContent = (filePath) => { /* implementation here */};

  const fetchFileContent = useCallback(async (fileName) => {
    try {
      setLoading(true);
      const response = await axios.get(`${BASE_URL}/file_content/${fileName}`, { responseType: 'arraybuffer' })
      const data = new Uint8Array(response.data)
      const workbook = XLSX.read(data, { type: 'array' })
      const jsonData = {};

      workbook.SheetNames.forEach((sheetName) => {
        const sheet = workbook.Sheets[sheetName];
        jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
      });

      setFileData(jsonData)
      setSelectedFileName(fileName); // Update the selected file name
    } 
    catch (error) { console.error('Error fetching file content:', error)} 
    finally { setLoading(false) }
  }, []);

  const fetchExcelFile = useCallback(async () => {
    try {
      if (!selectedFileName) return; // Check if a file is selected
      setLoading(true);
      const response = await axios.get(`${BASE_URL}/file_content/${selectedFileName}`, {
        responseType: 'blob',
      });
      const url = URL.createObjectURL(new Blob([response.data]));
      setExcelUrl(url);
    } 
    catch (error) { console.error('Error fetching Excel file:', error) } 
    finally { setLoading(false)  }
  }, [selectedFileName])

  const clearFileContent = () => { setFileData(null); setExcelUrl(null) };

  return (
    <div>
      <h2>File List</h2>
      <button onClick={fetchFileNames} disabled={loading}>
        {loading ? 'Fetching...' : 'List Files'}
      </button>
      <ul>
        {fileNames.map((fileName, index) => (
          <li key={index} onClick={() => fetchFileContent(fileName)} style={{ cursor: 'pointer' }}>
            {fileName}
          </li>
        ))}
      </ul>
      {fileData && (
        <div>
          <h3>File Content</h3>
          <pre>{JSON.stringify(fileData, null, 2)}</pre>
        </div>
      )}
      <button onClick={clearFileContent} disabled={loading || !fileData}>
        {loading ? 'Clearing...' : 'Clear Content'}
      </button>
      {excelUrl && (
        <iframe src={excelUrl} title="Excel Viewer" style={{ width: '100%', height: '600px', border: 'none' }}></iframe>
      )}
      {fileData && (
        <button onClick={fetchExcelFile} disabled={loading || !fileData}>
          {loading ? 'Fetching...' : 'Download Excel File'}
        </button>
      )}
    </div>
  );
};

export default FileList;
