import { useState, useEffect } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';

const useFetchFileContent = (BASE_URL) => {
    const [fileNames, setFileNames] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try { const response = await axios.get(`${BASE_URL}/file_list`);   setFileNames(response.data)  } 
            catch (error) { console.error('Error fetching file list:', error) }
        }
        fetchData()
    }, [BASE_URL])

    const fetchFileContent = async (fileName) => {
        try {
            const URL = `${BASE_URL}/file_content/${fileName}`;
            const response = await axios.get(URL, { responseType: 'arraybuffer' });
            const data = new Uint8Array(response.data);
            const workbook = XLSX.read(data, { type: 'array' });
            const jsonData = {};
            workbook.SheetNames.forEach((sheetName) => {
                const sheet = workbook.Sheets[sheetName];
                jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
            });
            return jsonData
        } catch (error) {  console.error('Error fetching file content:', error);   throw error }
    }
    return { fileNames, fetchFileContent };
};

export default useFetchFileContent;
