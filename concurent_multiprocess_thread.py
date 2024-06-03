import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageFilter
import time


# Function to resize and apply filter to images
async def process_image(img, idx):
    img_resized = img.resize((800, 600))  # Resize image
    img_filtered = img_resized.filter(ImageFilter.BLUR)  # Apply filter
    return idx, img_filtered

# Wrapper function to make process_image callable in the executor
def process_image_wrapper(img, idx):
    return asyncio.run(process_image(img, idx))

async def main():
    image = Image.new("RGB", (100, 100), "white")

    # Draw some basic patterns
    for i in range(0, 100, 10):
        for j in range(0, 100, 10):
            if (i + j) % 20 == 0: image.paste((0, 0, 0), (i, j, i + 10, j + 10))  # Draw a black square

    # Save the image
    image.save("generated_image.jpg")

    # List of processed images
    processed_images = [None] * 100

    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        # Submit tasks for parallel processing
        futures = [loop.run_in_executor(executor, process_image_wrapper, image.copy(), idx) for idx in range(100)]

        # Await all the futures concurrently
        results = await asyncio.gather(*futures)

        # Collect processed images
        for idx, processed_img in results:
            processed_images[idx] = processed_img

    # Directory to save processed images
    processed_dir = "processed_images"

    await make_dir(processed_dir)

    # Save processed images
    for idx, img in enumerate(processed_images):
        if img: img.save(f"{processed_dir}/processed_image_{idx}.jpg")

async def make_dir(processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    print(f"{processed_dir} Done")

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time} seconds.")


