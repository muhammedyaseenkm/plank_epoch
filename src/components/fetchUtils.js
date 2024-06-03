// src/components/fileUtils.js
const fetchFirstImage = (fileData) => {
    if (fileData.length > 0) {
      // Assuming each file object has a property 'images' which is an array of image URLs
      const firstImage = fileData[0].images[0]; // Assuming the first image of the first file is needed
      return firstImage;
    }
    return null; // Return null if fileData is empty or undefined
  };
  
  export { fetchFirstImage };
  