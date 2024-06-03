// src/components/sendImage.js
const handleFolderSelection = async (event, setFileNames) => {
    const files = event.target.files;
    const names = [];
    for (let i = 0; i < files.length; i++) {
      const formData = new FormData();
      formData.append('files', files[i]);
      try {
        const response = await fetch('http://127.0.0.1:5000/api/upload-images', {
          method: 'POST',
          body: formData
        });
        if (!response.ok) { throw new Error('Failed to upload file'); }
        const data = await response.json();
        names.push(data.uploaded_image);
        setFileNames([...names]); // Update fileNames state after each image upload
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };
  
  export { handleFolderSelection };
  