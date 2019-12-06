#!/usr/bin/env python3

"""
source come from https://www.liaoxuefeng.com/wiki/1016959663602400/1018491156860224
"""

import sys
import os
import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileMovedEvent


def log(s):
    print(f"[Reload] {s}")


class ReloadAppEventHandler(FileSystemEventHandler):
    def __init__(self, fn):
        super(ReloadAppEventHandler, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            # tmp file of PyCharm if enable "safe write"
            if getattr(event, 'dest_path', None) and event.dest_path.endswith('py___jb_old___'):
                return

            print(f"\n{'=' * 130}")
            # print('\n', '=' * 100)
            log(f"event: {event}")
            log(f"file changed: {event.src_path}")
            self.restart()


cmd = ['echo', 'ok']
process = None


def kill_process():
    global process
    if process:
        assert isinstance(process, subprocess.Popen)
        log(f"kill process [{process.pid}]")
        process.kill()
        process.wait()
        log(f"process ended with code [{process.returncode}]")
        process = None


def start_process():
    global cmd, process
    log(f"start process [{' '.join(cmd)}] ...")
    process = subprocess.Popen(cmd, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def restart_process():
    kill_process()
    start_process()


def start_watch(path):
    handler = ReloadAppEventHandler(restart_process)
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    log(f"watch dir {path} ...")
    start_process()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def main():
    global cmd
    argv = sys.argv[1:]
    if not argv:
        print("usage: python reloader.py ./main.py")
        sys.exit(0)

    if argv[0] != 'python3':
        argv.insert(0, 'python3')

    cmd = argv
    # path = os.path.abspath('..', '..')
    path = os.path.abspath(os.path.join(os.path.dirname(__name__), '..'))
    start_watch(path)


if __name__ == "__main__":
    main()
