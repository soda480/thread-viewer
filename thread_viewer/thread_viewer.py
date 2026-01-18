from list2term import Lines

BLOCK = "■"

class ThreadViewer(Lines):
    def __init__(self, thread_count, task_count, *, thread_prefix='thread_'):
        if thread_count < 1:
            raise ValueError('thread_count must be >= 1')
        if not thread_prefix:
            raise ValueError('thread_prefix must be non-empty')
        self._thread_count = thread_count
        self._task_count = task_count
        self._thread_prefix = thread_prefix
        self._thread_width = len(str(thread_count - 1))
        self._labels = ('Thread', 'Queued', 'Active', 'Closed')
        self._idx = {name: i for i, name in enumerate(self._labels)}
        x_axis = ' '.join(
            str(i).zfill(self._thread_width)
            for i in range(self._thread_count)
        )
        self._empty_cell = '-' * self._thread_width
        self._active_cell = BLOCK * self._thread_width
        self._threads = [self._empty_cell for _ in range(self._thread_count)]
        self._thread_row = self._idx['Thread']
        super().__init__(
            size=len(self._labels), show_x_axis=True, y_axis_labels=self._labels, x_axis=x_axis)

    def reset(self):
        for i in range(self._thread_count):
            self._threads[i] = self._empty_cell
        self._set('Queued', value=self._task_count)
        self._set('Active', value=0)
        self._set('Closed', value=0)
        self[self._thread_row] = self._get_threads_str()
    
    def run(self, thread_name):
        self._decrement('Queued')
        self._activate(thread_name)
        self._increment('Active')

    def done(self, thread_name):
        self._decrement('Active')
        self._deactivate(thread_name)
        self._increment('Closed')

    def _set_thread_cell(self, thread_name, active):
        n = self._get_thread_number(thread_name)
        self._threads[n] = self._active_cell if active else self._empty_cell
        self[self._thread_row] = self._get_threads_str()

    def _activate(self, thread_name):
        self._set_thread_cell(thread_name, True)

    def _deactivate(self, thread_name):
        self._set_thread_cell(thread_name, False)

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
    
    def _get_threads_str(self):
        return ' '.join(self._threads)
