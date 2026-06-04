import threading
import time


def scenario_1():
    output = []
    rlock = threading.RLock()

    counter = 0

    def inner():
        nonlocal counter

        with rlock:
            counter += 1

            output.append(
                f"inner function -> counter = {counter}"
            )

    def outer():
        with rlock:

            output.append(
                "outer function acquired RLock"
            )

            inner()

            output.append(
                "outer function released RLock"
            )

    threads = []

    for _ in range(5):
        thread = threading.Thread(target=outer)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 1,
        "title": "Thread Synchronization with RLock",
        "output": output,
        "explanation":
            "یک Thread می‌تواند چند بار یک RLock را دریافت کند. تابع outer قفل را می‌گیرد و سپس تابع inner دوباره همان قفل را می‌گیرد."
    }


def scenario_2():
    output = []
    rlock = threading.RLock()

    items_to_add = 10

    def add_item():
        nonlocal items_to_add

        with rlock:

            if items_to_add > 0:

                items_to_add -= 1

                output.append(
                    f"ADDED one item --> {items_to_add} items left"
                )

    threads = []

    for _ in range(10):
        thread = threading.Thread(
            target=add_item
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 2,
        "title": "Thread Synchronization with RLock",
        "output": output,
        "explanation":
            "RLock برای محافظت از متغیر مشترک استفاده شده است تا مقدار items_to_add به صورت ایمن تغییر کند."
    }


def scenario_3():
    output = []
    rlock = threading.RLock()

    counter = 0

    def level_3():
        nonlocal counter

        with rlock:
            counter += 1

            output.append(
                f"level_3 -> counter = {counter}"
            )

    def level_2():
        with rlock:

            output.append(
                "entered level_2"
            )

            level_3()

    def level_1():
        with rlock:

            output.append(
                "entered level_1"
            )

            level_2()

    thread = threading.Thread(
        target=level_1
    )

    thread.start()
    thread.join()

    return {
        "method": "thread",
        "section": 5,
        "scenario": 3,
        "title": "Thread Synchronization with RLock",
        "output": output,
        "explanation":
            "RLock اجازه می‌دهد یک Thread چندین بار و در توابع تو در تو همان قفل را دریافت کند."
    }