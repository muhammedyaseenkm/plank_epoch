from multiprocessing import Process, Queue, Value, Manager
from textblob import TextBlob

def worker(queue, shared_value, texts, sentiment_results):
    data = queue.get()
    print(f"Worker received: {data}")
    analyze_sentiment(texts[data], sentiment_results, data)
    shared_value.value += 1  

def analyze_sentiment(text, result_dict, index):
    """
    Function to analyze sentiment of a given text and store the result in a shared dictionary.
    """
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    result_dict[index] = sentiment_score

if __name__ == "__main__":
    # Define texts
    texts = [
        "I love this product, it's amazing!",
        "The service was terrible, never coming back again.",
        "The movie was okay, nothing special."
    ]
    
    queue = Queue()
    shared_int = Value('i', 0)  # Create a shared integer
    processes = []
    
    # Create a shared dictionary to store sentiment scores
    manager = Manager()
    sentiment_results = manager.dict()
    
    for _ in range(5):
        process = Process(target=worker, args=(queue, shared_int, texts, sentiment_results))
        processes.append(process)
        process.start()

    # Put some data into the queue for workers to process
    for i in range(5): 
        queue.put(i)

    for process in processes: 
        process.join()

    print(f"Final value: {shared_int.value}")  # Output: Final value: 5

    # Create processes for sentiment analysis
    processes = []
    for idx, _ in enumerate(texts):
        process = Process(target=analyze_sentiment, args=(texts[idx], sentiment_results, idx))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Print sentiment scores
    for idx, score in sentiment_results.items():
        print(f"Text {idx + 1}: Sentiment Score = {score}")
        if score >= 0.5:
            print(f"Text {idx+1} is positive")
        elif score <= 0:
            print(f"Text {idx+1} is Negative")
        else: 
            print(f"Text {idx+1} is Neutral")
