import time
from list2term import Lines

class ThreadRowView:

    def __init__(self, count=0, width=1, active_char='█', inactive_char=' '):
        if count < 0:
            raise ValueError('count must be >= 0')
        if width < 1:
            raise ValueError('width must be >= 1')
        self._active = active_char * width
        self._empty = inactive_char * width
        self._cells = [self._empty] * count
        self._x_axis = ' '.join(str(i).zfill(width) for i in range(count))

    def activate(self, n):
        self._check(n)
        self._cells[n] = self._active

    def deactivate(self, n, seconds=0):
        self._check(n)
        self._cells[n] = self._empty
        if seconds:
            time.sleep(seconds)

    def reset(self):
        self._cells[:] = [self._empty] * len(self._cells)

    def render(self):
        return ' '.join(self._cells)
       
    def _check(self, n):
        if n < 0 or n >= len(self._cells):
            raise ValueError(f'cell index out of range: {n}')
        
    @property
    def x_axis(self):
        return self._x_axis

class ThreadViewer(Lines):

    def __init__(self, thread_count=0, task_count=0, thread_prefix='thread_'):
        if thread_count < 1:
            raise ValueError('thread_count must be >= 1')
        if task_count < 0:
            raise ValueError('task_count must be >= 0')
        if not thread_prefix:
            raise ValueError('thread_prefix must be non-empty')

        self._task_count = task_count
        self._thread_prefix = thread_prefix
        self._thread_width = len(str(thread_count - 1))

        self._labels = ('Thread', 'Queued', 'Active', 'Closed')
        self._idx = {name: i for i, name in enumerate(self._labels)}

        self._thread_row_view = ThreadRowView(count=thread_count, width=self._thread_width)
        self._thread_row = self._idx['Thread']

        super().__init__(
            size=len(self._labels),
            show_x_axis=True,
            y_axis_labels=self._labels,
            x_axis=self._thread_row_view.x_axis)
        
    def __enter__(self):
        super().__enter__()
        self.reset()
        return self

    def reset(self):
        self._thread_row_view.reset()
        self._set('Queued', value=self._task_count)
        self._set('Active', value=0)
        self._set('Closed', value=0)
        self[self._thread_row] = self._thread_row_view.render()
    
    def run(self, thread_name):
        self._decrement('Queued')
        self._increment('Active')
        n = self._get_thread_number(thread_name)
        self._thread_row_view.activate(n)
        self[self._thread_row] = self._thread_row_view.render()

    def done(self, thread_name):
        self._decrement('Active')
        self._increment('Closed')
        n = self._get_thread_number(thread_name)
        self._thread_row_view.deactivate(n, seconds=.1)
        self[self._thread_row] = self._thread_row_view.render()

    def _decrement(self, name):
        i = self._idx[name]
        self[i] = str(int(self[i]) - 1)

    def _increment(self, name):
        i = self._idx[name]
        self[i] = str(int(self[i]) + 1)

    def _set(self, name, value=0):
        i = self._idx[name]
        self[i] = str(value)

    def _get_thread_number(self, thread_name):
        if not thread_name.startswith(self._thread_prefix):
            raise ValueError(f'Unexpected thread name: {thread_name!r}')
        return int(thread_name[len(self._thread_prefix):])

