from celery import Celery
import time

# Initialize Celery
app = Celery('tasks', broker='amqp://guest:guest@rabbitmq//')

@app.task
async def process_task(task_id):
    # Simulate processing
    print(f"Processing task {task_id}")
    time.sleep(2)
    print(f"Task {task_id} done")

