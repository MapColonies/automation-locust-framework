from locust import HttpUser, task, between, events
import json
import queue
import threading

# --- Config ---
LOG_FILE = "all_requests.jsonl"
log_queue = queue.Queue()

# --- Background Logger ---
def background_writer():
    with open(LOG_FILE, "a") as f:
        while True:
            data = log_queue.get()
            if data == "STOP":
                break
            f.write(json.dumps(data) + "\n")
            log_queue.task_done()

# Start background thread
threading.Thread(target=background_writer, daemon=True).start()

# --- Listeners ---
@events.request_success.add_listener
def log_success(request_type, name, response_time, response_length, response, context, **kwargs):
    request_data = {
        "type": request_type,
        "name": name,
        "url": response.request.url,
        "method": response.request.method,
        "request_headers": dict(response.request.headers),
        "request_body": response.request.body.decode("utf-8") if response.request.body else None,
        "status_code": response.status_code,
        "response_time_ms": response_time,
        "response_length": response_length,
        "response_body": response.text
    }
    log_queue.put(request_data)

@events.request_failure.add_listener
def log_failure(request_type, name, response_time, exception, context, **kwargs):
    request_data = {
        "type": request_type,
        "name": name,
        "status": "FAILED",
        "error": str(exception),
        "response_time_ms": response_time
    }
    log_queue.put(request_data)

# --- Example Locust test ---
class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def send_request(self):
        data = {"foo": "bar"}
        self.client.get("/api/test", json=data)