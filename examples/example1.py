import sys
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from thread_viewer import ThreadViewer

def process_task(item, viewer):
    thread_name = threading.current_thread().name
    viewer.run(thread_name)
    try:
        seconds = random.uniform(.1, 1)
        time.sleep(seconds)
        return seconds
    finally:
        viewer.done(thread_name)

def main():
    args = dict(a.split('=', 1) for a in sys.argv[1:])
    workers = int(args['workers'])
    tasks = int(args['tasks'])

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix='thread') as executor:
        with ThreadViewer(
            thread_count=workers,
            task_count=tasks,
            thread_prefix='thread_'
        ) as viewer:
            futures = [executor.submit(process_task, task, viewer) for task in range(tasks)]
            return [future.result() for future in futures]

if __name__ == '__main__':
    main()

