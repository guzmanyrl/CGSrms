# check_task_status.py

from celery.result import AsyncResult

# Replace with your task ID
task_id = '0d5c3612-f82a-41d9-b954-104cc6fa11f8'
result = AsyncResult(task_id)

# Check if the task is finished
if result.ready():
    print("Task finished:", result.result)  # This will print the result of the task if it's successful
else:
    print("Task is still processing.")
