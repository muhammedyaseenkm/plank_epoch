import React, { useState } from 'react';
import { DataFrame } from 'pandas-js';
import axios from 'axios';
import * as XLSX from 'xlsx';

const BASE_URL = 'Your_Base_URL'; // Replace 'Your_Base_URL' with your actual base URL

const ExcelViewer = () => {
    const [fileContent, setFileContent] = useState(null);

    const handleFileNameClick = async (fileName) => {
        try {
            const response = await axios.get(`${BASE_URL}/file_content/${fileName}`, { responseType: 'arraybuffer' });
            const data = new Uint8Array(response.data);
            const workbook = XLSX.read(data, { type: 'array' });
            const jsonData = {};

            workbook.SheetNames.forEach((sheetName) => {
                const sheet = workbook.Sheets[sheetName];
                jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
            });

            const df = new DataFrame(jsonData);
            console.log(df.toString());

            setFileContent(jsonData);
        } catch (error) {
            console.error('Error fetching file content:', error);
        }
    };

    // Convert JSON data to Excel
    const convertJSONToExcel = (jsonData, fileName) => {
        const newWorkbook = XLSX.utils.book_new();

        for (const sheetName in jsonData) {
            const sheetData = jsonData[sheetName];
            const worksheet = XLSX.utils.json_to_sheet(sheetData);
            XLSX.utils.book_append_sheet(newWorkbook, worksheet, sheetName);
        }

        XLSX.writeFile(newWorkbook, `${fileName}.xlsx`);
    };

    const handleDownloadExcel = () => {
        if (fileContent) {
            convertJSONToExcel(fileContent, 'example');
        }
    };

    const handleDownloadJSON = () => {
        if (fileContent) {
            // Convert JSON data to JSON file
            const jsonDataString = JSON.stringify(fileContent, null, 2);
            const blob = new Blob([jsonDataString], { type: 'application/json' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = `example.json`;
            link.click();
        }
    };

    return (
        <div>
            <button onClick={() => handleFileNameClick('example')}>Fetch Excel Data</button>
            <button onClick={handleDownloadExcel}>Download Excel</button>
            <button onClick={handleDownloadJSON}>Download JSON</button>

            {fileContent && (
                <iframe
                    src={`data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${fileContent}`}
                    style={{ width: '100%', height: '500px' }}
                    title="Excel Viewer"
                />
            )}
        </div>
    );
};

export default ExcelViewer;
