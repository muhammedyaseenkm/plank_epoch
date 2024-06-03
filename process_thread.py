import os
import asyncio
from multiprocessing import Process, Pipe
from PIL import Image, ImageFilter
import threading

# Function to resize and apply filter to images
def process_image(img, idx, conn):
    img_resized = img.resize((800, 600))  # Resize image
    img_filtered = img_resized.filter(ImageFilter.BLUR)  # Apply filter
    conn.send((idx, img_filtered))
    conn.close()

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

    # Create pipes
    pipes = [Pipe() for _ in range(100)]

    # Spawn processes for parallel processing
    processes = []
    threads = []
    for idx, (conn_parent, conn_child) in enumerate(pipes):
        p = Process(target=process_image, args=(image.copy(), idx, conn_child))
        t = threading.Thread(target=p.start)
        t.start()
        processes.append((p, conn_parent))
        threads.append(t)

    # Collect processed images
    for p, conn in processes:
        idx, processed_img = conn.recv()
        processed_images[idx] = processed_img

    # Directory to save processed images
    processed_dir = "processed_images"

    await make_dir(processed_dir)

    # Save processed images
    for idx, img in enumerate(processed_images):
        if img: img.save(f"{processed_dir}/processed_image_{idx}.jpg")

    # Wait for all threads to finish
    for t in threads:
        t.join()

async def make_dir(processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    print(f"{processed_dir} Done")

if __name__ == "__main__":
    import time
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time} seconds.")