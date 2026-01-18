from thread_viewer.thread_viewer import ThreadViewer

with ThreadViewer(12, 50) as thread_viewer:
    thread_viewer.run('thread_5')
    thread_viewer.run('thread_3')
    thread_viewer.run('thread_0')
    thread_viewer.run('thread_1')
    thread_viewer.run('thread_6')
    thread_viewer.run('thread_7')
    thread_viewer.run('thread_11')
    thread_viewer.run('thread_10')
    thread_viewer.run('thread_9')
    thread_viewer.done('thread_6')
    thread_viewer.done('thread_11')
