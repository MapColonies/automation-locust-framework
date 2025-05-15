import csv
import os
import threading
import queue

from common.config.config import config_obj

MAX_ROWS_PER_FILE = config_obj["default"].MAX_ROWS_PER_FILE
OUTPUT_DIR = config_obj["default"].OUTPUT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

_data_queue = queue.Queue()
_stop_event = threading.Event()


class _CSVWriterThread(threading.Thread):
    def __init__(self, queue, output_dir, max_rows):
        super().__init__()
        self.queue = queue
        self.output_dir = output_dir
        self.max_rows = max_rows
        self.file_index = 0
        self.row_count = 0
        self.file = None
        self.writer = None

    def rotate_file(self):
        if self.file:
            self.file.close()
        self.file_index += 1
        self.row_count = 0
        file_path = os.path.join(self.output_dir, f"requests_{self.file_index}.csv")
        self.file = open(file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=["method", "url", "params", "body","headers"])
        self.writer.writeheader()

    def run(self):
        self.rotate_file()
        while not _stop_event.is_set() or not self.queue.empty():
            try:
                data = self.queue.get(timeout=1)
                if self.row_count >= self.max_rows:
                    self.rotate_file()
                self.writer.writerow(data)
                self.row_count += 1
                self.queue.task_done()
            except queue.Empty:
                continue
        if self.file:
            self.file.close()


_writer_thread = _CSVWriterThread(_data_queue, OUTPUT_DIR, MAX_ROWS_PER_FILE)
_writer_thread.start()


def log_request(method: str, url: str, params: dict, body: dict , headers: dict):
    """Public function to be called from tests."""

    _data_queue.put({
        "method": method,
        "url": url,
        "params": str(params),
        "body": str(body),
        "headers": str(headers)

    })


def shutdown_logger():
    """Call this on test stop to flush and cleanly stop the logger."""
    _stop_event.set()
    _writer_thread.join()


def insert_request_log(func):
    def wrapper(*args, **kwargs):
        log_request(**kwargs)
        res = func(*args, **kwargs)
        return res

    return wrapper