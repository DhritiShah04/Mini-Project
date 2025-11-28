import asyncio
import threading
import os
import random
import string
from locust import task, between, User
from function_actions import FunctionActions
import gevent

# --- Async Boilerplate ---
def thread_func(loop, coro, *args, **kwargs):
    future = asyncio.run_coroutine_threadsafe(coro(*args, **kwargs), loop)
    event = gevent.event.Event()
    future.add_done_callback(lambda _: event.set())
    event.wait()
    return future.result()

def run_asyncio(loop, coro, *args, **kwargs):
    return thread_func(loop, coro, *args, **kwargs)

class FunctionUser(User):
    print("Locust class 'Function User' initialized.")
    wait_time = between(2, 5)
    host = "http://localhost"

    shared_loop = None
    shared_thread = None
    initialized_pid = None

    # --- FILTERED DATASET (Lenovo Only) ---
    dataset = [
        # --- Lenovo (Existing & New) ---
        "Lenovo IdeaPad Slim 5", "Lenovo ThinkBook 14s", "Lenovo Yoga Slim 7i",
        "Lenovo IdeaPad Slim 3", "Lenovo Legion 5", "Lenovo IdeaPad Flex 5",
        "Lenovo ThinkPad X1 Carbon", "Lenovo LOQ 15", "Lenovo Yoga 9i",
        "Lenovo Legion 7i", "Lenovo ThinkPad T14 Gen 4", "Lenovo IdeaPad Gaming 3",
        "Lenovo Yoga 7i", "Lenovo ThinkPad E16",

        # --- Dell ---
        "Dell XPS 13", "Dell XPS 15", "Dell Inspiron 16", "Dell G15 Gaming",
        "Alienware x14", "Dell Latitude 7440", "Dell Inspiron 14 Plus",

        # --- HP ---
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_pid = os.getpid()
        if FunctionUser.initialized_pid != current_pid:
            FunctionUser.initialized_pid = current_pid
            FunctionUser.shared_loop = asyncio.new_event_loop()
            FunctionUser.shared_thread = threading.Thread(
                target=FunctionUser.shared_loop.run_forever,
                daemon=True
            )
            FunctionUser.shared_thread.start()

        self.loop = FunctionUser.shared_loop
        self.actions = FunctionActions(self)
   
    @task(1)
    def task_get_reviews_with_cache(self):
        # Pick a random Lenovo model
        target_model = random.choice(self.dataset)

        run_asyncio(self.loop, self.actions.analyze_reviews_with_cache, [target_model])
    
    @task(1)
    def task_get_reviews_without_cache(self):
        # Pick a random Lenovo model
        target_model = random.choice(self.dataset)

        run_asyncio(self.loop, self.actions.analyze_reviews_without_cache, [target_model])