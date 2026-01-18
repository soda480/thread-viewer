import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from thread_viewer.thread_viewer import ThreadViewer

def process_item(item, viewer):
    thread_name = threading.current_thread().name  # e.g. "thread_3"
    viewer.run(thread_name)
    try:
        seconds = random.uniform(1, 2)
        time.sleep(seconds)
        return seconds
    finally:
        viewer.done(thread_name)

def main():
    items = 75
    num_threads = 12

    with ThreadPoolExecutor(max_workers=num_threads, thread_name_prefix='thread') as executor:
        with ThreadViewer(thread_count=num_threads, task_count=items, thread_prefix='thread_') as viewer:
            futures = [executor.submit(process_item, item, viewer) for item in range(items)]
            return [future.result() for future in futures]

if __name__ == "__main__":
    main()
