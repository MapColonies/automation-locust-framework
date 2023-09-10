# import json
# from json import JSONDecodeError
#
# from locust import HttpUser, task
# class Tasks(HttpUser):
#     @task
#     def task(self):
#         with self.client.get("https://www.ynet.co.il") as response:
#             try:
#                 result = json.loads(response.content)
#                 if len(result["result"]) == 0:
#                     response.failure(result)
#                     # log.error(result)
#             except (TypeError, JSONDecodeError) as err:
#                 response.failure(response.text)
# log.error(f'{type(err).__name__} because of : {response.status_code} - {response.text}')


#
# from locust import HttpUser, task
#
# class MyUser(HttpUser):
#     @task
#     def my_task(self):
#         response = self.client.get("https://www.ynet.co.il")
#
#         # Check the response content type
#         content_type = response.headers.get("Content-Type", "")
#
#         if "application/json" not in content_type:
#             # Mark the request as a failure with a custom reason including the response text
#             response.failure(f"Content-Type is not text/html. Response: {response.text}")
#
# from locust import HttpUser, task
#
#
# class MyUser(HttpUser):
#     @task
#     def my_task(self):
#         response = self.client.get("https://www.ynet.co.il")
#
#         # Check the response content type
#         content_type = response.headers.get("Content-Type", "")
#
#         if "application/json" not in content_type:
#             # Mark the request as a failure with a custom reason including the response text
#             failure_reason = f"Content-Type is not text/html. Response: {response.text}"
#             response.failure(failure_reason)


from locust import HttpUser, task


class MyUser(HttpUser):
    @task
    def my_task(self):
        with self.client.get("https://www.ynet.co.il", catch_response=True) as response:
            content_type = response.headers.get("Content-Type", "")
            if content_type != "application/json":
                response.failure("Not a json")
            elif response.elapsed.total_seconds() > 0.5:
                response.failure("Request took too long")
