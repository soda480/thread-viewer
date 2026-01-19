# `thread-viewer`
A lightweight terminal UI for visualizing thread pool activity in real time.

thread-viewer shows:
* how many tasks are queued, active, and completed
* which threads are currently active
* live activity even under high throughput (via color changes)

It’s built on top of [list2term](https://pypi.org/project/list2term/) and designed to work naturally with `ThreadPoolExecutor` and real thread names.

## Features

* Real-time terminal visualization
* Works with real thread names (no fake IDs)
* Colorized activity to make fast thread reuse visible
* Minimal API: `run()` / `done()`
* No background render loop
* No sleeps required in workers
* Safe to use in long-running jobs

## Installation

```bash
pip install thread-viewer
```

## [Example](https://github.com/soda480/thread-viewer/blob/main/examples/example1.py)

<details><summary>Code</summary>

```Python
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from thread_viewer.thread_viewer import ThreadViewer

def process_item(item, viewer):
    thread_name = threading.current_thread().name  # e.g. "thread_3"
    viewer.run(thread_name)
    try:
        seconds = random.uniform(.1, 1)
        time.sleep(seconds)
        return seconds
    finally:
        viewer.done(thread_name)

def main():
    items = 120
    num_threads = 24

    with ThreadPoolExecutor(max_workers=num_threads, thread_name_prefix='thread') as executor:
        with ThreadViewer(
            thread_count=num_threads,
            task_count=items,
            thread_prefix='thread_'
        ) as viewer:
            futures = [executor.submit(process_item, item, viewer) for item in range(items)]
            return [future.result() for future in futures]

if __name__ == "__main__":
    main()
```
</details>

![example4c](https://github.com/soda480/thread-viewer/blob/main/docs/images/example1.gif?raw=true)

* Each cell represents a thread
* Active threads are shown as blocks
* Every activation changes color so you can see reuse
* Counts updater live

## API Overview

```Python
class ThreadViewer(
    thread_count,               # number of worker threads
    task_count,                 # total number of tasks expected
    thread_prefix='thread_'     # prefix used to extract thread index
)
```

Creates a terminal viewer. Default works with `ThreadPoolExecutor(thread_name_prefix='thread')`

### Core Methods

| Method | Description |
| --- | --- |
| `run(thread_name)`  |	Marks a task as started on a thread. |
| `done(thread_name)` | Marks a task as completed on a thread. |

### Context manager

Always use ThreadViewer as a context manager:

```Python
with ThreadViewer(...) as viewer:
```
This ensures proper terminal setup and cleanup.

## How It Works

* Uses list2term.Lines for efficient terminal updates
* Each thread maps to a fixed cell index
* On every activation:
    * the cell is updated
    * a new foreground color is chosen (different from the previous one)
* This makes activity visible even when threads never truly go idle

No polling. No timers. Just state changes.

## When to Use

Good fit if you want:
* visibility into thread pool behavior
* confirmation that work is parallelized
* insight into hot threads or uneven scheduling
* a lightweight alternative to logging spam

Not intended to replace profilers or tracing tools.

## Limitations

* Terminal-only
* ANSI colors required
* Not meant for very narrow terminals
* Visualization is informational, not a scheduler

## Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t thread-viewer:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
thread-viewer:latest \
bash
```

Execute the dev pipeline:
```sh
make dev
```