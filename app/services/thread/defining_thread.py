import threading
import time
import random


def scenario_1():
    output = []

    def my_func(thread_number):
        output.append(
            f"my_func called by thread N°{thread_number}"
        )

    threads = []

    for i in range(10):
        thread = threading.Thread(
            target=my_func,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 1,
        "title": "Defining a Thread",
        "output": output,
        "explanation":
            "10 thread به صورت همزمان اجرا می‌شوند."
    }


def scenario_2():
    output = []

    def my_func(thread_number):

        time.sleep(
            random.uniform(0.1, 1)
        )

        output.append(
            f"my_func called by thread N°{thread_number}"
        )

    threads = []

    for i in range(10):
        thread = threading.Thread(
            target=my_func,
            args=(i,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 2,
        "title": "Defining a Thread",
        "output": output,
        "explanation":
            "هر thread دارای delay تصادفی است."
    }


def scenario_3():
    output = []

    def my_func(thread_number):
        output.append(
            f"my_func called by thread N°{thread_number}"
        )

    for i in range(10):

        thread = threading.Thread(
            target=my_func,
            args=(i,)
        )

        thread.start()
        thread.join()

    return {
        "method": "thread",
        "section": 1,
        "scenario": 3,
        "title": "Defining a Thread",
        "output": output,
        "explanation":
            "به علت join اجرای thread ها ترتیبی می‌شود."
    }