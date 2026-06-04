import threading
import time
import os
import random


class MyThread(threading.Thread):

    def __init__(self, thread_number, delay):
        super().__init__()
        self.thread_number = thread_number
        self.delay = delay
        self.output = None

    def run(self):
        self.output.append(
            f"---> Thread#{self.thread_number} running, belonging to process ID {os.getpid()}"
        )

        time.sleep(self.delay)

        self.output.append(
            f"---> Thread#{self.thread_number} over"
        )


def scenario_1():
    output = []
    threads = []

    for i in range(1, 10):
        thread = MyThread(i, 0.5)
        thread.output = output
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("End")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 1,
        "title": "Defining a Thread Subclass",
        "output": output,
        "explanation":
            "در این سناریو یک کلاس از threading.Thread ارث‌بری می‌کند و متد run بازنویسی می‌شود. همه thread ها در یک process مشترک اجرا می‌شوند."
    }


def scenario_2():
    output = []
    threads = []

    for i in range(1, 10):
        delay = random.uniform(0.1, 1)
        thread = MyThread(i, delay)
        thread.output = output
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    output.append("End")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 2,
        "title": "Defining a Thread Subclass",
        "output": output,
        "explanation":
            "در این سناریو برای هر thread زمان اجرای تصادفی در نظر گرفته شده است. بنابراین ترتیب پایان thread ها در هر اجرا متفاوت خواهد بود."
    }


def scenario_3():
    output = []

    for i in range(1, 10):
        thread = MyThread(i, 0.2)
        thread.output = output
        thread.start()
        thread.join()

    output.append("End")

    return {
        "method": "thread",
        "section": 3,
        "scenario": 3,
        "title": "Defining a Thread Subclass",
        "output": output,
        "explanation":
            "در این سناریو بعد از start هر thread بلافاصله join اجرا می‌شود. بنابراین thread ها به جای اجرای همزمان، یکی‌یکی اجرا می‌شوند."
    }