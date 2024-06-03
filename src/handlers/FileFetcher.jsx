import React, { useEffect, useState } from 'react';
import useFetchFileContent from './useFetchFileContent';

const MyComponent = () => {
    const { fetchFileContent } = useFetchFileContent('your_base_url_here');
    const [jsonData, setJsonData] = useState(null); // State to store fetched JSON data

    useEffect(() => {
        const getFileContent = async () => {
            try {
                const data = await fetchFileContent('example.xlsx');
                setJsonData(data); // Update state with fetched data
            } catch (error) {
                console.error('Error:', error);
            }
        };
        getFileContent();
    }, [fetchFileContent]);

    return (
        <div>
            {jsonData && (
                <pre>{JSON.stringify(jsonData, null, 2)}</pre>
            )}
        </div>
    );
};

export default MyComponent;
