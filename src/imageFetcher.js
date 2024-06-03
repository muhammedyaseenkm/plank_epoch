// imageFetcher.js
export const fetchImageFromServer = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/image/url');
      if (!response.ok) {
        throw new Error('Failed to fetch image');
      }
      const imageData = await response.blob();
      const imageUrl = URL.createObjectURL(imageData);
      return imageUrl;
    } catch (error) {
      console.error('Error fetching image:', error);
      return null;
    }
  };
  