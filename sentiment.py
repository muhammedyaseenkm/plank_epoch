from multiprocessing import Process, Queue, Value, Manager
from textblob import TextBlob



def worker(queue, shared_value, texts, sentiment_results):
    while True:
        data = queue.get()
        if data is None:
            break
        print(f"Worker received: {data}")
        analyze_sentiment(texts[data], sentiment_results, data)
        with shared_value.get_lock():
            shared_value.value += 1

def analyze_sentiment(text, result_dict, index):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    result_dict[index] = sentiment_score

if __name__ == '__main__':
    manager = Manager()
    sentiment_results = manager.dict()
    queue = manager.Queue()
    shared_int = manager.Value('i', 0)  # Create a shared integer

    texts = [
        "I love this product, it's amazing!",
        "The service was terrible, never coming back again.",
        "The movie was okay, nothing special."
    ]

    for i, text in enumerate(texts):
        queue.put(i)

    num_processes = 2  # Adjust the number of processes as needed
    processes = []
    for _ in range(num_processes):
        p = Process(target=worker, args=(queue, shared_int, texts, sentiment_results))
        processes.append(p)
        p.start()

    # Signal workers to stop
    for _ in range(num_processes):
        queue.put(None)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("Sentiment Analysis Results:", sentiment_results)