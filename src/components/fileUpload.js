// Constants
const CHUNK_SIZE = 1024 * 1024 * 5; // 5 MB

// Function to handle chunked file upload
const handleChunkUpload = async (file) => {
  // Chunk the file
  const chunks = [];
  let start = 0;
  while (start < file.size) {
    chunks.push(file.slice(start, start + CHUNK_SIZE));
    start += CHUNK_SIZE;
  }

  // Upload each chunk
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

// Function to handle folder selection
const handleFolderSelection = async (files, setFileNames) => {
  const names = [];

  // Iterate over selected files and upload each in chunks
  for (let i = 0; i < files.length; i++) {
    names.push(files[i].name);
    await handleChunkUpload(files[i]); // Call handleChunkUpload function
  }

  // Update state with file names 
  setFileNames(names);
};

// Function to fetch the first image
const fetchFirstImage = async (setImageSrc) => {
  // Function remains the same
};

// Export the functions
export { handleFolderSelection, fetchFirstImage };
